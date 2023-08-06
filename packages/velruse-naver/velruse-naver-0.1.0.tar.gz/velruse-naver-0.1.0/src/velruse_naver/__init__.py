# -*- coding: utf-8 -*-
#
#   velruse-naver: velruse provider for NAVER OAuth2
#   Copyright (C) 2015-2018 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import logging
import uuid

from pyramid.httpexceptions import HTTPFound
from pyramid.security import NO_PERMISSION_REQUIRED
import requests

from velruse.api import AuthenticationComplete
from velruse.api import AuthenticationDenied
from velruse.api import register_provider
from velruse.exceptions import CSRFError
from velruse.exceptions import ThirdPartyFailure
from velruse.settings import ProviderSettings
from velruse.utils import flat_url

__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class NaverAuthenticationComplete(AuthenticationComplete):
    """Naver OAuth 2.0 auth complete"""


def includeme(config):
    config.add_directive('add_naver_login', add_naver_login)
    config.add_directive('add_naver_login_from_settings',
                         add_naver_login_from_settings)


def add_naver_login_from_settings(config, prefix='velruse.naver.'):
    settings = config.registry.settings
    p = ProviderSettings(settings, prefix)
    p.update('consumer_key', required=True)
    p.update('consumer_secret', required=True)
    p.update('login_path')
    p.update('callback_path')
    config.add_naver_login(**p.kwargs)


def add_naver_login(
    config,
    consumer_key=None,
    consumer_secret=None,
    login_path='/login/naver',
    callback_path='/login/naver/callback',
    name='naver'
):
    provider = NaverOAuth2Provider(
        name,
        consumer_key,
        consumer_secret,
    )
    config.add_route(provider.login_route, login_path)
    config.add_view(
        provider,
        attr='login',
        route_name=provider.login_route,
        permission=NO_PERMISSION_REQUIRED,
    )
    config.add_route(
        provider.callback_route,
        callback_path,
        use_global_views=True,
        factory=provider.callback,
    )
    register_provider(config, name, provider)


class NaverOAuth2Provider(object):

    def __init__(self, name, consumer_key, consumer_secret):
        self.name = name
        self.type = 'naver_oauth2'
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.login_route = 'velruse.{}-login'.format(name)
        self.callback_route = 'velruse.{}-callback'.format(name)

    def login(self, request):
        request.session['velruse.state'] = state = uuid.uuid4().hex

        auth_url = flat_url(
            'https://nid.naver.com/oauth2.0/authorize',
            response_type='code',
            client_id=self.consumer_key,
            redirect_uri=request.route_url(self.callback_route),
            state=state
        )
        return HTTPFound(location=auth_url)

    def callback(self, request):
        session_state = request.session.pop('velruse.state', None)
        request_state = request.GET.get('state')
        if not session_state or session_state != request_state:
            raise CSRFError()

        code = request.GET.get('code')
        if not code:
            return AuthenticationDenied(
                reason='unknown',  # TODO
                provider_name=self.name,
                provider_type=self.type
            )

        token_url = flat_url(
            'https://nid.naver.com/oauth2.0/token',
            **{
                'grant_type': 'authorization_code',
                'client_id': self.consumer_key,
                'client_secret': self.consumer_secret,
                'redirect_uri': request.route_url(self.callback_route),
                'code': code,
                'state': request_state,
            }
        )
        r = requests.get(
            token_url,
            headers={
                'x-naver-client-id': self.consumer_key,
                'x-naver-client-secret': self.consumer_secret,
            },
        )

        if r.status_code != 200:
            raise ThirdPartyFailure('Status {}: {}'.format(
                r.status_code, r.content
            ))

        token_data = r.json()
        if 'access_token' not in token_data:
            error = token_data['error']
            error_description = token_data['error_description']
            raise ThirdPartyFailure('{}: {}'.format(
                error, error_description
            ))
        access_token = token_data['access_token']

        r = requests.get('https://openapi.naver.com/v1/nid/me', headers={
            'Authorization': 'Bearer {}'.format(access_token),
        })
        if r.status_code != 200:
            raise ThirdPartyFailure('Status {}: {}'.format(
                r.status_code, r.content
            ))

        result = r.json()
        logger.debug('result: %r', result)

        code = result['resultcode']
        message = result['message']
        if code != '00':
            raise ThirdPartyFailure('Fetching profile failed: {} {}'.format(
                code, message
            ))

        profile = result['response']

        cred = {
            'oauthAccessToken': access_token,
        }
        return NaverAuthenticationComplete(
            profile=profile,
            credentials=cred,
            provider_name=self.name,
            provider_type=self.type
        )
