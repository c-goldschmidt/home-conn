import asyncio
import json
import logging
import os

import aiohttp
from aiohttp import web

from server.utils.constants import STATIC_DIR
from server.utils.module import Module
from server.utils.ssl_module import SSLMixin

_logger = logging.getLogger('Module: Webserver')
app_logger = logging.getLogger('Module: Webserver - APP')


class CustomSocketResponse(web.WebSocketResponse):
    def __bool__(self):
        return not self.closed


class WebserverModule(SSLMixin, Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.server = None
        self.keep_running = True
        self.is_running = False

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

    async def create_socket_connection(self, request):
        headers = request.headers.copy()
        if not all([
            headers.get('connection').lower() == 'upgrade',
            headers.get('upgrade').lower() == 'websocket',
            request.method == 'GET',
        ]):
            return web.HTTPBadRequest(reason='expected a websocket connection')

        ws_server = CustomSocketResponse()
        await ws_server.prepare(request)
        await self.context_manager.socket_manager.register(ws_server)

        async for ws_message in ws_server:
            if ws_message.type != aiohttp.WSMsgType.TEXT:
                continue

            message = ws_message.data
            _logger.debug(f'received "{message}"')

            try:
                message = json.loads(message)
                await self.context_manager.run_cmd(message, ws_server)
            except ValueError:
                _logger.error('message faulty')
            except Exception as e:
                _logger.error(e)

    async def _start_server(self):
        runner = web.AppRunner(self.server)

        _logger.debug('setup runner')
        await runner.setup()

        _logger.debug('starting server on {}:{} (ssl: {})'.format(
            self.context_manager.config.server['domain'],
            self.context_manager.config.server.int('port'),
            self.get_ssl_context(),
        ))

        site = web.TCPSite(
            runner,
            host=self.context_manager.config.server['domain'],
            port=self.context_manager.config.server.int('port'),
            ssl_context=self.get_ssl_context(),
        )

        _logger.debug('start site')
        await site.start()

    async def start(self):
        _logger.info('initializing...')

        self.server = web.Application(logger=app_logger)
        self.server.router.add_route('get', '/__callback__', self.handle_callback)
        self.server.router.add_route('get', '/', self.serve_frontend)
        self.server.router.add_route('get', '/ws', self.create_socket_connection)
        self.server.router.add_route('get', '/wss', self.create_socket_connection)
        self.server.router.add_routes([web.static(f'/static', STATIC_DIR)])

        await self._start_server()
        _logger.info('Server running on {}:{} (ssl: {})'.format(
            self.context_manager.config.server['domain'],
            self.context_manager.config.server.int('port'),
            self.get_ssl_context(),
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

