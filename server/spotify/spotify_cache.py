
import requests
import spotipy
from cachecontrol import CacheControl


class SpotifyCached(spotipy.Spotify):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session = CacheControl(requests.Session())
