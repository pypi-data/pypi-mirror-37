# -*- coding: utf-8 -*-
"""
session authentication
"""
from django.conf import settings
from django.contrib.auth.signals import user_logged_in

from .models import Token as AuthToken, get_or_create_token
from .settings import auth_settings

# Login Hooks here:
def create_session_token(sender, user, request, issuer="Django-Session", **kwargs):
    auth_token = get_or_create_token(user, issuer=issuer)
    auth_token.expireTime = AuthToken.update_expiration() # Expiration time based on auth_settings
    auth_token.save()
    request.session['username'] = auth_token.user.username
    request.session['token'] = auth_token.key
    return auth_token


# Instantiate the login hook here.
# TODO: Investigate if this is the cause of 'the atmoadmin bug'
user_logged_in.connect(create_session_token)
