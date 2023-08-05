"""
authentication response views.
"""
import json
from datetime import datetime
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect

import logging
logger = logging.getLogger(__name__)

from .models import get_or_create_token, userCanEmulate
from .models import Token as AuthToken
from .protocol.cas import cas_validateUser, cas_loginRedirect, get_cas_oauth_client
from .protocol.globus import globus_logout, globus_authorize, globus_validate_code
from .protocol.ldap import ldap_validate
from .settings import auth_settings
from .exceptions import Unauthorized

#GLOBUS Views


def globus_login_redirect(request):
    next_url = request.GET.get('next', '/application')
    request.session['next'] = next_url

    return globus_authorize(request)

def globus_logout_redirect(request):
    logout_redirect_url = request.GET.get('next', '/application')
    if 'http' not in logout_redirect_url:
        logout_redirect_url = settings.SERVER_URL + logout_redirect_url
    return globus_logout(logout_redirect_url)

def globus_callback_authorize(request):
    """
    TODO: This logic 'lets the auth token escape'
    May need to refactor this...
    """
    code = request.GET.get('code')
    try:
        user_token = globus_validate_code(request)
    except Unauthorized as bad_code:
        logger.exception("Globus login failed to validate code: %s" % bad_code)
        app_name = auth_settings.APP_NAME
        site_name = auth_settings.SITE_NAME
        return HttpResponse(
            "In order to use %s you must consent to "
            "releasing your identity details from Globus to %s."
            % (app_name, site_name), status=401)
    if not user_token:
        # Redirect out of the OAuth loop
        return HttpResponseRedirect(auth_settings.LOGOUT_REDIRECT_URL)
    user = authenticate(key=user_token.key)
    django_login(request, user)

    # Apply newly created AuthToken to session
    request.session['username'] = user_token.user.username
    request.session['access_token'] = user_token.key
    # Redirect to 'next'
    next_url = request.session.get('next', '/application')
    return HttpResponseRedirect(next_url)


#CAS+OAuth Views



def o_callback_authorize(request):
    """
    Authorize a callback from an OAuth IdP
    ( Uses request.META to route which IdP is in use )
    """
    # IF globus --> globus_callback_authorize
    referrer = request.META.get('HTTP_REFERER','no-referrer')
    if 'globus' in referrer or auth_settings.GLOBUS_AUTH_URL:
        return globus_callback_authorize(request)
    return cas_callback_authorize(request)


def login_redirect(request, redirect_to):
    all_backends = settings.AUTHENTICATION_BACKENDS
    if 'django_cyverse_auth.authBackends.CASLoginBackend' in all_backends:
        return cas_loginRedirect(request, redirect_to)
    else:
        return HttpResponseRedirect(redirect_to)



def o_login_redirect(request):
    oauth_client = get_cas_oauth_client()
    url = oauth_client.authorize_url()
    return HttpResponseRedirect(url)


def cas_callback_authorize(request):
    """
    Authorize a callback (From CAS IdP)
    """
    if 'code' not in request.GET:
        # TODO - Maybe: Redirect into a login
        return HttpResponse("")
    oauth_client = get_cas_oauth_client()
    oauth_code = request.GET['code']
    # Exchange code for ticket
    access_token, expiry_date = oauth_client.get_access_token(oauth_code)
    if not access_token:
        logger.warn("The Code %s is invalid/expired. Attempting another login."
                    % oauth_code)
        return o_login_redirect(request)
    # Exchange token for profile
    user_profile = oauth_client.get_profile(access_token)
    if not user_profile or "username" not in user_profile:
        logger.error("AccessToken is producing an INVALID profile!"
                     " Check the CAS server and caslib.py for more"
                     " information.")
        # NOTE: Make sure this redirects the user OUT of the loop!
        return login(request)
    # ASSERT: A valid OAuth token gave us the Users Profile.
    # Now create an AuthToken and return it
    username = user_profile["username"]
    auth_token = get_or_create_token(username, access_token, expiry_date, issuer="CAS+OAuth")
    # Set the username to the user to be emulated
    # to whom the token also belongs
    request.session['username'] = username
    request.session['token'] = auth_token.key
    return HttpResponseRedirect(settings.REDIRECT_URL + "/application/")


#Token Authentication Views


@csrf_exempt
def token_auth(request):
    """
    VERSION 2 AUTH
    Authentication is based on the POST parameters:
    * Username (Required)
    * Password (Not Required if CAS authenticated previously)

    NOTE: This authentication is SEPARATE from
    django model authentication
    Use this to give out tokens to access the API
    """
    token = request.POST.get('token', None)

    username = request.POST.get('username', None)
    # CAS authenticated user already has session data
    # without passing any parameters
    if not username:
        username = request.session.get('username', None)

    password = request.POST.get('password', None)
    # LDAP Authenticate if password provided.
    if username and password:
        if ldap_validate(username, password):
            token = get_or_create_token(username, issuer='API')
            expireTime = token.issuedTime + auth_settings.TOKEN_EXPIRY_TIME
            auth_json = {
                'token': token.key,
                'username': token.user.username,
                'expires': expireTime.strftime("%b %d, %Y %H:%M:%S")
            }
            return HttpResponse(
                content=json.dumps(auth_json),
                status=201,
                content_type='application/json')
        else:
            logger.debug("[LDAP] Failed to validate %s" % username)
            return HttpResponse("LDAP login failed", status=401)

    #    logger.info("User %s already authenticated, renewing token"
    #                % username)

    # ASSERT: Token exists here
    if token:
        expireTime = token.issuedTime + auth_settings.TOKEN_EXPIRY_TIME
        auth_json = {
            'token': token.key,
            'username': token.user.username,
            'expires': expireTime.strftime("%b %d, %Y %H:%M:%S")
        }
        return HttpResponse(
            content=json.dumps(auth_json),
            content_type='application/json')

    if not username and not password:
        # The user and password were not found
        # force user to login via CAS
        return cas_loginRedirect(request, '/auth/')

    if cas_validateUser(username):
        logger.info("CAS User %s validated. Creating auth token" % username)
        token = createAuthToken(username)
        expireTime = token.issuedTime + auth_settings.TOKEN_EXPIRY_TIME
        auth_json = {
            'token': token.key,
            'username': token.user.username,
            'expires': expireTime.strftime("%b %d, %Y %H:%M:%S")
        }
        return HttpResponse(
            content=json.dumps(auth_json),
            content_type='application/json')
    else:
        logger.debug("[CAS] Failed to validate - %s" % username)
        return HttpResponse("CAS Login Failure", status=401)


def auth1_0(request):
    """
    VERSION 1 AUTH -- DEPRECATED
    Authentication is based on the values passed in to the header.
    If successful, the request is passed on to auth_response
    CAS Authentication requires: "x-auth-user" AND "x-auth-cas"
    LDAP Authentication requires: "x-auth-user" AND "x-auth-key"

    NOTE(esteve): Should we just always attempt authentication by cas,
    then we dont send around x-auth-* headers..
    """
    logger.debug("Auth Request")
    if 'HTTP_X_AUTH_USER' in request.META\
            and 'HTTP_X_AUTH_CAS' in request.META:
        username = request.META['HTTP_X_AUTH_USER']
        if cas_validateUser(username):
            del request.META['HTTP_X_AUTH_CAS']
            return auth_response(request)
        else:
            logger.debug("CAS login failed - %s" % username)
            return HttpResponse("401 UNAUTHORIZED", status=401)

    if 'HTTP_X_AUTH_KEY' in request.META\
            and 'HTTP_X_AUTH_USER' in request.META:
        username = request.META['HTTP_X_AUTH_USER']
        x_auth_key = request.META['HTTP_X_AUTH_KEY']
        if ldap_validate(username, x_auth_key):
            return auth_response(request)
        else:
            logger.debug("LDAP login failed - %s" % username)
            return HttpResponse("401 UNAUTHORIZED", status=401)
    else:
        logger.debug("Request did not have User/Key"
                     " or User/CAS in the headers")
        return HttpResponse("401 UNAUTHORIZED", status=401)


def auth_response(request):
    """
    Create a new AuthToken for the user, then return the Token & API URL
    AuthTokens will expire after a predefined time
    (See #/auth/utils.py:auth_settings.TOKEN_EXPIRY_TIME)
    AuthTokens will be re-newed if
    the user is re-authenticated by CAS at expiry-time
    """
    logger.debug("Creating Auth Response")
    api_server_url = settings.API_SERVER_URL
    # login validation
    response = HttpResponse()

    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = 1000
    response['Access-Control-Allow-Headers'] = '*'

    response['X-Server-Management-Url'] = api_server_url
    response['X-Storage-Url'] = "http://"
    response['X-CDN-Management-Url'] = "http://"
    token = str(uuid.uuid4())
    username = request.META['HTTP_X_AUTH_USER']
    response['X-Auth-Token'] = token
    # New code: If there is an 'emulate_user' parameter:
    if 'HTTP_X_EMULATE_USER' in request.META:
        # AND user has permission to emulate
        if userCanEmulate(username):
            logger.debug("EMULATION REQUEST:"
                         "Generating AuthToken for %s -- %s" %
                         (request.META['HTTP_X_EMULATE_USER'],
                          username))
            response['X-Auth-User'] = request.META['HTTP_X_EMULATE_USER']
            response['X-Emulated-By'] = username
            # then this token is for the emulated user
            auth_user_token = AuthToken(
                user=request.META['HTTP_X_EMULATE_USER'],
                issuedTime=datetime.now(),
                remote_ip=request.META['REMOTE_ADDR'],
                api_server_url=api_server_url
            )
        else:
            logger.warn("EMULATION REQUEST:User deemed Unauthorized : %s" %
                        (username,))
            # This user is unauthorized to emulate users - Don't create a
            # token!
            return HttpResponse("401 UNAUTHORIZED TO EMULATE", status=401)
    else:
        # Normal login, no user to emulate
        response['X-Auth-User'] = username
        auth_user_token = AuthToken(
            user=username,
            issuedTime=datetime.now(),
            remote_ip=request.META['REMOTE_ADDR'],
            api_server_url=api_server_url
        )

    auth_user_token.save()
    return response
