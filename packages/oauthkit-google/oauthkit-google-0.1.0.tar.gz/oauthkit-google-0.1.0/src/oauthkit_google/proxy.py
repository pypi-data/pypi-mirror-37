# -*- coding: utf-8 -*-
#
#   oauthkit-google: OAuthKit for Google
#   Copyright (C) 2015-2018 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from jsonable_objects.proxy import JsonableProxy
from zope.interface import implementer

from .interfaces import IGoogleClientSecret
from .interfaces import IGoogleTokenResponse


@implementer(IGoogleClientSecret)
class GoogleClientSecret(JsonableProxy):

    @classmethod
    def validate(cls, d):
        proxy = cls(d)
        proxy.client_id
        proxy.client_secret
        proxy.project_id
        proxy.auth_uri
        proxy.token_uri
        proxy.auth_provider_x509_cert_url
        proxy.redirect_uris
        return proxy

    @property
    def client_id(self):
        return str(self.__jsonable__['client_id'])

    @property
    def client_secret(self):
        return str(self.__jsonable__['client_secret'])

    @property
    def project_id(self):
        return str(self.__jsonable__['project_id'])

    @property
    def auth_uri(self):
        return str(self.__jsonable__['auth_uri'])

    @property
    def token_uri(self):
        return str(self.__jsonable__['token_uri'])

    @property
    def auth_provider_x509_cert_url(self):
        return str(self.__jsonable__['auth_provider_x509_cert_url'])

    @property
    def redirect_uris(self):
        return self.__jsonable__['redirect_uris']


@implementer(IGoogleTokenResponse)
class GoogleTokenResponse(JsonableProxy):

    @classmethod
    def validate(cls, d):
        proxy = cls(d)
        proxy.access_token
        proxy.expires_in
        proxy.token_type
        proxy.refresh_token
        return proxy

    @property
    def access_token(self):
        return str(self.__jsonable__['access_token'])

    @property
    def expires_in(self):
        return int(self.__jsonable__['expires_in'])

    @property
    def token_type(self):
        return str(self.__jsonable__['token_type'])

    @property
    def refresh_token(self):
        refresh_token = self.__jsonable__.get('refresh_token')
        if refresh_token is not None:
            return str(refresh_token)
