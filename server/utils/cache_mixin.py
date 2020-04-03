import hashlib
import json
import logging
import os
import time


class CacheMixin:
    cache_file = None
    timeout = None
    _logger = logging.getLogger('Some CacheMixin implementer')

    def cache_miss(self, *args, **kwargs):
        raise NotImplementedError

    def _save(self):
        with open(self.cache_file, 'w') as f:
            f.write(json.dumps(self.entries))

    def _load(self):
        if not os.path.isfile(self.cache_file):
            return

        with open(self.cache_file, 'r') as f:
            self.entries = json.loads(f.read())

        self._clean()

    def _clean(self):
        keys_to_remove = []
        for key in self.entries:
            if self._too_old(self.entries[key]):
                self._logger.debug(f'discard key "{key}" (too old)')
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.entries[key]
        self._save()

    def _too_old(self, entry):
        return time.time() - entry['created'] > self.timeout

    def get(self, *args, **kwargs):
        key = self._key(*args, **kwargs)

        if key not in self.entries or self._too_old(self.entries[key]):
            self.entries[key] = {
                'entry': self.cache_miss(*args, **kwargs),
                'created': time.time()
            }
            self._save()
        return self.entries[key]['entry']

    def has(self, *args, **kwargs):
        key = self._key(*args, **kwargs)
        return key in self.entries and not self._too_old(self.entries[key])

    def _key(self, *args, **kwargs):
        return hashlib.sha1(json.dumps({'args': args, 'kwargs': kwargs}).encode('UTF-8')).hexdigest()

    def invalidate(self, *args, **kwargs):
        key = self._key(*args, **kwargs)
        if key in self.entries:
            del self.entries[key]
            self._save()
