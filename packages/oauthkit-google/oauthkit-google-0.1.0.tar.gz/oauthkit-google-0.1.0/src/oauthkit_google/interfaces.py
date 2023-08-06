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

from zope.interface import Attribute
from zope.interface import Interface


class IGoogleClientSecret(Interface):

    client_id = Attribute('Client ID')
    client_secret = Attribute('Client Secret')
    project_id = Attribute('Project ID')
    auth_uri = Attribute('Auth URI')
    token_uri = Attribute('Token URI')
    auth_provider_x509_cert_url = Attribute(
        'Auth Provider X509 Certificate URL'
    )
    redirect_uris = Attribute(
        'Redirect URIs.'
    )


class IGoogleTokenResponse(Interface):

    access_token = Attribute('Access token')
    expires_in = Attribute('Seconds in which the token expires')
    token_type = Attribute('Token type')
    refresh_token = Attribute('Refresh token')
