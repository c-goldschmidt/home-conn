import json
import logging
import os
import time

from server.utils.cache_mixin import CacheMixin
from server.utils.constants import CACHE_PATH

_logger = logging.getLogger('UriCache')


class UriCache(CacheMixin):
    def __init__(self, spotify):
        self.entries = {}
        self.sp = spotify

        self.timeout = 24 * 60 * 60
        self.cache_file = os.path.join(CACHE_PATH, '_uri_cache')
        self._load()
        self._logger = logging.getLogger('UriCache')

    @staticmethod
    def get_type(uri):
        split = uri.split(':')
        if len(split) > 1:
            return uri.split(':')[1]
        return None

    def cache_miss(self, uri):
        uri_type = self.get_type(uri)

        if uri_type == 'playlist':
            return self.sp.playlist(uri)
        if uri_type == 'track':
            return self.sp.track(uri)
        if uri_type == 'artist':
            return self.sp.artist(uri)
        if uri_type == 'album':
            return self.sp.album(uri)

        return None
