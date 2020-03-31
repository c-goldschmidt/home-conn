import logging

_logger = logging.getLogger('UriCache')


class UriCache:
    def __init__(self, spotify):
        self.entries = {}
        self.sp = spotify

    @staticmethod
    def get_type(uri):
        split = uri.split(':')
        if len(split) > 1:
            return uri.split(':')[1]
        return None

    def get(self, uri):
        if uri not in self.entries:
            _logger.info(f'cache miss: {uri}')
            self.entries[uri] = self.fetch(uri)
        return self.entries[uri]

    def fetch(self, uri):
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
