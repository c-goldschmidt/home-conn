import logging

import spotipy

from server.spotify.devices import SpotifyDevices
from server.spotify.spotify_auth import SpotifyAuth
from server.spotify.spotify_cache import SpotifyCached
from server.spotify.uri_cache import UriCache
from server.utils.base_cmd import BaseCmd
_logger = logging.getLogger('SpotifyCMD')


def ignore_exception(func):
    async def wrapper(instance, *args, **kwargs):
        try:
            if not instance.auth.auth_token:
                return None
            return await func(instance, *args, **kwargs)
        except spotipy.SpotifyException as e:
            _logger.error(e)

    return wrapper


def if_token_async(func):
    async def wrapper(instance, *args, **kwargs):
        if instance.auth.auth_token:
            return await func(instance, *args, **kwargs)
        return None
    return wrapper


def if_token_sync(func):
    def wrapper(instance, *args, **kwargs):
        if instance.auth.auth_token:
            return func(instance, *args, **kwargs)
        return None
    return wrapper


class SpotifyCMD(BaseCmd):
    TYPE = 'spotify'

    def __init__(self, context_manager):
        super().__init__(context_manager)
        self.auth = SpotifyAuth(context_manager)

        self.sp = SpotifyCached(oauth_manager=self.auth.sp_oauth)
        self.uri_cache = UriCache(self.sp)

        self.current_status = None
        self.devices = SpotifyDevices()
        self.last_device_id = None
        self.last_valid_playback = None

        self._update_current()
        self._update_devices()

    @if_token_sync
    def _update_current(self):
        self.current_status = self.sp.current_playback()
        if self.current_status:
            device = self.current_status.get('device', {})
            self.devices.update([device] if device else [])
            self.last_device_id = device.get('id')
            self.last_valid_playback = self.current_status
        else:
            self.current_status = {
                **self.last_valid_playback,
                'is_playing': False,
            } if self.last_valid_playback else None

    async def check_auth_required(self, socket):
        if self.auth.auth_token:
            return

        url = self.auth.sp_oauth.get_authorize_url()
        await self.context_manager.socket_manager.send_to_socket(socket, {
            'type': 'spotify_auth_required',
            'payload': url,
        })

    @if_token_sync
    def _update_devices(self):
        self.devices.update(self.sp.devices()['devices'])

    @ignore_exception
    @if_token_async
    async def update_playing_state(self):
        if not self.context_manager.user_manager.has_logged_in:
            # no one needs to know this right now...
            return

        self._update_current()

        for user in self.context_manager.user_manager.user_list:
            if user.socket:
                await self._send_status(user.socket)

    @ignore_exception
    @if_token_async
    async def update_devices(self):
        if not self.context_manager.user_manager.has_logged_in:
            # no one needs to know this right now...
            return

        self._update_devices()
        for user in self.context_manager.user_manager.user_list:
            if user.socket:
                await self._send_devices(user.socket)

    async def token_callback(self, code):
        self.auth.token_callback(code)

        admin = self.context_manager.user_manager.get_admin()
        if self.auth.auth_token and admin and admin.socket:
            await self.context_manager.socket_manager.send_to_socket(admin.socket, {
                'type': 'spotify_auth_required',
                'payload': None,
            })

    @if_token_async
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
            await self._send_devices(sender)
        if message['cmd'] == 'play':
            await self._play(message['payload'])
        if message['cmd'] == 'add_to_playlist':
            await self._add_to_playlist(message['payload'])
        if message['cmd'] == 'resolve_uri':
            await self._resolve_uri(message['payload'], sender)
        if message['cmd'] == 'switch_device':
            await self._switch_to_device(message['payload'])

    async def _send_status(self, to_socket):
        await self.context_manager.socket_manager.send_to_socket(to_socket, {
            'type': 'spotify_status_change',
            'payload': self.current_status,
        })

    async def _send_devices(self, to_socket):
        await self.context_manager.socket_manager.send_to_socket(to_socket, {
            'type': 'spotify_devices_result',
            'payload': self.devices.known_devices,
        })

    @ignore_exception
    async def _resolve_uri(self, uri, sender):
        await self.context_manager.socket_manager.send_to_socket(sender, {
            'type': 'spotify_uri_result',
            'payload': self.uri_cache.get(uri),
        })

    @ignore_exception
    async def _next(self):
        print(self.sp.next_track())
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
        for playlist in playlists['items']:
            await self._check_main_playlist(playlist)

        await self.context_manager.socket_manager.send_to_socket(sender, {
            'type': 'spotify_playlist_result',
            'payload': playlists,
        })

    @ignore_exception
    async def _check_main_playlist(self, playlist):
        playlist['is_main_playlist'] = playlist['id'] == self.context_manager.config.spotify['playlist_id']
        if not playlist['is_main_playlist']:
            return

        tracks = self.sp.playlist_tracks(playlist['id'])
        playlist['tracks'] = tracks

    @ignore_exception
    async def _switch_to_device(self, payload):
        self.sp.transfer_playback(payload['id'], True)
        await self.update_devices()
        await self.update_playing_state()

    @ignore_exception
    async def _add_to_playlist(self, payload):
        me = self.sp.me()
        self.sp.user_playlist_add_tracks(
            me['id'],
            self.context_manager.config.spotify['playlist_id'],
            [payload['id']]
        )

        updated_playlist = self.sp.playlist(self.context_manager.config.spotify['playlist_id'])
        self.uri_cache.invalidate(updated_playlist['uri'])
        await self._check_main_playlist(updated_playlist)

        for user in self.context_manager.user_manager.user_list:
            if user.socket:
                await self.context_manager.socket_manager.send_to_socket(user.socket, {
                    'type': 'spotify_update_playlist',
                    'payload': updated_playlist,
                })

    @ignore_exception
    async def _play(self, payload):
        uri_type = self.uri_cache.get_type(payload['uri'])
        if uri_type in ('album', 'artist', 'playlist'):
            self.sp.start_playback(
                device_id=self.last_device_id,
                context_uri=payload['uri'],
                position_ms=None,
                offset=None,
                uris=None,
            )
        if uri_type == 'track':
            self.sp.start_playback(
                device_id=self.last_device_id,
                position_ms=None,
                offset=None,
                uris=[payload['uri']],
            )

        await self.update_playing_state()
