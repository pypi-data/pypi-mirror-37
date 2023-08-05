# -*- coding: utf-8 -*-
"""
Settings for the authentication app.
"""
from datetime import timedelta

from django.conf import settings
from django.test.signals import setting_changed
import sys, os

APP_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, APP_DIRECTORY)

USER_SETTINGS = getattr(settings, 'AUTHENTICATION', {})


DEFAULTS =  {
    # General
    "APP_NAME": "Iplantauth Application",
    "SITE_NAME": "",
    "TOKEN_EXPIRY_TIME": timedelta(days=1),
    "CAS_SERVER": None,
    "API_SERVER_URL": None,
    "LOGOUT_REDIRECT_URL": None,
    # OAUTH
    "OAUTH_CLIENT_KEY": None,
    "OAUTH_CLIENT_SECRET": None,
    "OAUTH_CLIENT_CALLBACK": None,

    # KEYSTONE
    "KEYSTONE_SERVER": None,
    "KEYSTONE_DOMAIN_NAME": "Default",
    # LDAP
    "LDAP_SERVER": None,
    "LDAP_SERVER_DN": None,
    #GLOBUS
    "GLOBUS_MAPPING_FILE": None,
    "GLOBUS_OAUTH_ID": None,
    "GLOBUS_OAUTH_SECRET": None,
    "GLOBUS_OAUTH_CREDENTIALS_SCOPE": None,
    "GLOBUS_OAUTH_ATMOSPHERE_SCOPE": None,
    "GLOBUS_TOKENINFO_URL": None,
    "GLOBUS_TOKEN_URL": None,
    "GLOBUS_AUTH_URL": None,
}


class ReadOnlyAttrDict(dict):
    __getattr__ = dict.__getitem__

new_settings = DEFAULTS.copy()
new_settings.update(USER_SETTINGS)


auth_settings = ReadOnlyAttrDict(new_settings)


def reload_settings(*args, **kwargs):
    global auth_settings
    setting_name, values = kwargs['setting'], kwargs['value']
    if setting_name == "AUTHENTICATION":
        defaults = DEFAULTS.copy()
        auth_settings = ReadOnlyAttrDict(defaults.update(values))

setting_changed.connect(reload_settings)

__all__ = ('auth_settings', )
