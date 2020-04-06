import logging
import os
from time import sleep

import spotipy

from server.utils.constants import CACHE_PATH

_logger = logging.getLogger('SpotifyAuth')


class NoBrowserOAuth(spotipy.SpotifyOAuth):
    def get_authorization_code(self, response=None):
        if response:
            return self.parse_response_code(response)

        raise NotImplementedError()


class SpotifyAuth:

    def __init__(self, context_manager):
        self.context_manager = context_manager

        config = self.context_manager.config
        cache_path = os.path.join(CACHE_PATH, '_spotify_token')

        scope = [
            'user-modify-playback-state',
            'user-read-playback-state',
            'user-read-currently-playing',
            'playlist-read-private',
            'playlist-read-collaborative',
            'playlist-modify-private',
            'playlist-modify-public',
        ]

        self.sp_oauth = NoBrowserOAuth(
            config.spotify['client_id'],
            config.spotify['client_secret'],
            redirect_uri=config.spotify['callback_url'],
            scope=' '.join(scope),
            cache_path=cache_path,
            show_dialog=True,
        )

        self.auth_token = self.fetch_token()

    def token_callback(self, code):
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
