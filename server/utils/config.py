import configparser
import logging

from server.utils.ssl_module import SSLMixin

_logger = logging.getLogger('Config')


class Config(SSLMixin, configparser.ConfigParser):

    def __init__(self, filename='config.ini'):
        super().__init__()
        self.filename = filename
        self._load()

        self.spotify = self['spotify']
        self.ports = self['ports']
        self.server = self['server']
        self.ssl = self['ssl']

        self.prod_mode = self.server['prod_mode'].lower() == 'true'
        if self.prod_mode:
            self.ssl_enabled = self.verify_ssl()

    @property
    def url_prefix(self):
        prefix = self.server.get('url_prefix')
        if not prefix:
            prefix = ''
        elif prefix[0] != '/':
            prefix = f'/{prefix}'
        return prefix

    def verify_ssl(self):
        cert_path = self.ssl.get('base_path')
        if not cert_path:
            _logger.warning('in prod_mode, using ssl is strongly advised!')
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
