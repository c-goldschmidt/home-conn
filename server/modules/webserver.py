import asyncio
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
        self.keep_running = True
        self.is_running = False

    @staticmethod
    def _server_print(message, *args, **kwargs):
        app_logger.info(message.split('\n')[0])

    async def handle_callback(self, request):
        code = request.query.get('code')

        if code:
            await self.context_manager.spotify.token_callback(code)

        return web.Response(text=f'''<!doctype html>
        <html lang="en">
            <body>You can close this window now.</body>
            <script>window.close()</script>
        </html>
        ''', content_type='text/html')

    async def serve_frontend(self, request):
        with open(os.path.join(STATIC_DIR, 'index.html'), 'r') as file:
            return web.Response(text=file.read(), content_type='text/html')

    async def _start_server(self):
        runner = web.AppRunner(self.server)

        _logger.info('setup runner')
        await runner.setup()

        _logger.info('starting server on {}:{} (ssl: {})'.format(
            self.context_manager.config.server['domain'],
            self.context_manager.config.ports['webserver'],
            self.get_ssl_context(),
        ))

        site = web.TCPSite(
            runner,
            self.context_manager.config.server['domain'],
            self.context_manager.config.ports.int('webserver', 8080),
            ssl_context=self.get_ssl_context(),
        )

        _logger.info('start site')
        await site.start()

    async def start(self):
        _logger.info('initializing...')

        self.server = web.Application(logger=app_logger)
        self.server.router.add_route('get', '/__callback__', self.handle_callback)
        self.server.router.add_route('get', '/', self.serve_frontend)
        self.server.router.add_routes([web.static(f'/static', STATIC_DIR)])

        await self._start_server()
        _logger.info('Server running on {}:{}'.format(
            self.context_manager.config.server['domain'],
            self.context_manager.config.ports['webserver'],
        ))

        self.keep_running = True
        self.is_running = True
        while self.keep_running:
            await asyncio.sleep(30)
        self.is_running = False

    async def stop(self):
        _logger.info('shutting down server')
        await self.server.shutdown()
        await self.server.cleanup()

        self.keep_running = False
        while self.is_running:
            await asyncio.sleep(1)

