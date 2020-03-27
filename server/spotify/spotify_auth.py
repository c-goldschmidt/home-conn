import logging
import os
from time import sleep

import spotipy

from server.utils.constants import CACHE_PATH

_logger = logging.getLogger('SpotifyAuth')


class NoBrowserOAuth(spotipy.SpotifyOAuth):
    __response = None

    def set_response(self, response):
        self.__response = response

    def get_authorization_code(self, response=None):
        if response:
            return self.parse_response_code(response)

        _logger.warning(f'need auth: {self.get_authorize_url()}')
        while not self.__response:
            sleep(10)
        return self.__response


class SpotifyAuth:

    def __init__(self, context_manager):
        self.context_manager = context_manager

        config = self.context_manager.config
        cache_path = os.path.join(CACHE_PATH, config.spotify['username'])

        self.sp_oauth = NoBrowserOAuth(
            config.spotify['client_id'],
            config.spotify['client_secret'],
            redirect_uri=self._get_callback_url(config),
            username=config.spotify['username'],
            scope='user-modify-playback-state user-read-playback-state user-read-currently-playing',
            cache_path=cache_path,
            show_dialog=True,
        )

        self.auth_token = self.fetch_token()

    def _get_callback_url(self, config):
        prefix = self.context_manager.config.url_prefix
        protocol = "https" if config.ssl_enabled else "http"

        callback_url = f'{protocol}://{config.server["callback_domain"]}{prefix}/__callback__'
        return callback_url

    def token_callback(self, code):
        self.sp_oauth.set_response(code)
        self.auth_token = self.sp_oauth.get_access_token(code, as_dict=False)
        _logger.info('got a new token :)')

    def fetch_token(self):
        token_info = self.sp_oauth.get_cached_token()

        if not token_info:
            auth_url = self.sp_oauth.get_authorize_url()

            if self.context_manager.config.server.get('no_browser'):
                _logger.info(f'open {auth_url} in browser for auth...')
                return None

            try:
                import webbrowser
                webbrowser.open(auth_url)
            except ImportError:
                _logger.info(f'open {auth_url} in browser for auth...')
            return None
        else:
            _logger.info('using cached token')

        return token_info
