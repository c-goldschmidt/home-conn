import logging

import spotipy

from server.spotify.spotify_auth import SpotifyAuth
from server.utils.base_cmd import BaseCmd
_logger = logging.getLogger('SpotifyCMD')


def ignore_exception(func):
    async def wrapper(instance, *args, **kwargs):
        try:
            if not instance.auth.auth_token:
                return None
            await func(instance, *args, **kwargs)
        except spotipy.SpotifyException as e:
            _logger.error(e)

    return wrapper


class SpotifyCMD(BaseCmd):
    TYPE = 'spotify'

    def __init__(self, context_manager):
        super().__init__(context_manager)
        self.auth = SpotifyAuth(context_manager)

        self.sp = spotipy.Spotify(oauth_manager=self.auth.sp_oauth)

        self.current_status = None
        self.last_device_id = None
        self._update_current()

    def _update_current(self):
        if not self.auth.auth_token:
            return

        self.current_status = self.sp.current_playback()
        if self.current_status:
            device = self.current_status.get('device', {})
            self.last_device_id = device.get('id')

    @ignore_exception
    async def update_playing_state(self):
        if not self.context_manager.user_manager:
            # no one needs to know this right now...
            return

        self._update_current()

        for user in self.context_manager.user_manager.user_list:
            if user.socket:
                await self._send_status(user.socket)

    def token_callback(self, code):
        self.auth.token_callback(code)

    async def run_cmd(self, message, sender):
        if message['cmd'] == 'fetch_status':
            await self._send_status(sender)
        if message['cmd'] == 'next':
            await self._next()
        if message['cmd'] == 'prev':
            await self._prev()
        if message['cmd'] == 'pause':
            await self._pause()
        if message['cmd'] == 'resume':
            await self._resume()
        if message['cmd'] == 'fetch_playlists':
            await self._fetch_playlists(sender)
        if message['cmd'] == 'fetch_devices':
            await self._fetch_devices(sender)
        if message['cmd'] == 'play':
            await self._play(message['payload'])

    async def _send_status(self, to_socket):
        await self.context_manager.socket_manager.send_to_socket(to_socket, {
            'type': 'spotify_status_change',
            'payload': self.current_status,
        })

    @ignore_exception
    async def _next(self):
        self.sp.next_track()
        await self.update_playing_state()

    @ignore_exception
    async def _prev(self):
        self.sp.previous_track()
        await self.update_playing_state()

    @ignore_exception
    async def _pause(self):
        self.sp.pause_playback()
        await self.update_playing_state()

    @ignore_exception
    async def _resume(self):
        self.sp.start_playback()
        await self.update_playing_state()

    @ignore_exception
    async def _fetch_playlists(self, sender):
        playlists = self.sp.current_user_playlists()
        await self.context_manager.socket_manager.send_to_socket(sender, {
            'type': 'spotify_playlist_result',
            'payload': playlists,
        })

    @ignore_exception
    async def _fetch_devices(self, sender):
        devices = self.sp.devices()
        await self.context_manager.socket_manager.send_to_socket(sender, {
            'type': 'spotify_devices_result',
            'payload': devices,
        })

    async def _play(self, payload):
        self.sp.start_playback(
            device_id=self.last_device_id,
            context_uri=payload['uri'],
            position_ms=None,
            offset=None,
            uris=None,
        )
        await self.update_playing_state()
