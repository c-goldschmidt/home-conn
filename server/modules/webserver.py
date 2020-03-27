import logging
import os

from aiohttp import web

from server.utils.constants import STATIC_DIR
from server.utils.module import Module
from server.utils.ssl_module import SSLMixin

_logger = logging.getLogger('Module: Webserver')
app_logger = logging.getLogger('Module: Webserver - APP')


class WebserverModule(SSLMixin, Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.server = None

    @staticmethod
    def _server_print(message, *args, **kwargs):
        app_logger.info(message.split('\n')[0])

    async def handle_callback(self, request):
        code = request.query.get('code')

        if code:
            self.context_manager.spotify.token_callback(code)

        return web.HTTPFound(location='/')

    async def serve_frontend(self, request):
        _logger.info(f'serve {request}')
        with open(os.path.join(STATIC_DIR, 'index.html'), 'r') as file:
            return web.Response(text=file.read(), content_type='text/html')

    async def start(self):
        _logger.info('initializing...')

        self.server = web.Application(logger=app_logger)
        self.server.router.add_route('get', '/__callback__', self.handle_callback)
        self.server.router.add_route('get', '/', self.serve_frontend)
        self.server.router.add_routes([web.static('/static', STATIC_DIR)])

        await web._run_app(
            self.server,
            host=self.context_manager.config.server["domain"],
            port=self.context_manager.config.ports['webserver'],
            print=self._server_print,
            ssl_context=self.get_ssl_context(),
        )
        _logger.info('init OK')

    async def stop(self):
        _logger.info('shutting down server')
        await self.server.shutdown()
        await self.server.cleanup()
