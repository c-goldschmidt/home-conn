import os
import ssl


class SSLMixin:
    context_manager = None
    __ssl_context = None

    def get_ssl_context(self, config=None):
        if self.__ssl_context:
            return self.__ssl_context

        if not config and self.context_manager:
            config = self.context_manager.config

        cert_path, crt_file, key_file = self._get_paths(config)
        self.__ssl_context = ssl.create_default_context(
            ssl.Purpose.CLIENT_AUTH,
            capath=cert_path,
        )
        self.__ssl_context.load_cert_chain(crt_file, key_file)

        return self.__ssl_context

    def _get_paths(self, config):
        cert_path = config.ssl.get('base_path')
        if not cert_path or not os.path.isdir(cert_path):
            raise ValueError(f'no such directory: {cert_path}')

        crt_file = os.path.join(cert_path, config.ssl.get('crt_filename'))
        key_file = os.path.join(cert_path, config.ssl.get('key_filename'))

        if not os.path.isfile(crt_file):
            raise ValueError(f'no such file: {cert_path}')

        if not os.path.isfile(crt_file):
            raise ValueError(f'no such file: {key_file}')

        return cert_path, crt_file, key_file
