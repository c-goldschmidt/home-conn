import configparser
import logging

from server.utils.ssl_module import SSLMixin

_logger = logging.getLogger('Config')


class ConfigPart(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def bool(self, key, true_if_not_set=False):
        default = 'true' if true_if_not_set else 'false'
        return self.get(key, default).lower() == 'true'

    def __getitem__(self, key):
        return self.get(key, None)


class Config(SSLMixin, configparser.ConfigParser):

    def __init__(self, filename='config.ini'):
        super().__init__()
        self.filename = filename
        self._load()

        self.spotify = ConfigPart(self['spotify'])
        self.ports = ConfigPart(self['ports'])
        self.server = ConfigPart(self['server'])
        self.ssl = ConfigPart(self['ssl'] if 'ssl' in self else {})

        self.prod_mode = self.server.bool('prod_mode')
        if self.prod_mode:
            self.ssl_enabled = self.verify_ssl()

    def verify_ssl(self):
        if not self.ssl:
            _logger.warning('in prod_mode, using ssl is strongly advised!')
            return False

        cert_path = self.ssl.get('base_path')
        if not cert_path:
            _logger.warning('base_path not set')
            return False

        try:
            self.get_ssl_context(self)
            return True
        except (TypeError, ValueError) as e:
            _logger.warning(f'error loading ssl context: {e}')

        return False

    def _load(self):
        super().read(self.filename)

    def save(self):
        with open(self.filename, 'w') as configfile:
            super().write(configfile)
