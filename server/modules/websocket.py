import json
import logging
import websockets

from server.utils.module import Module
from server.utils.ssl_module import SSLMixin

_logger = logging.getLogger('Module: WebSocket')


class WebsocketModule(SSLMixin, Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.server = None

    async def websocket_client(self, sock, *_):
        _logger.info('received connection')
        # register(sock) sends send_file_update() to websocket
        await self.context_manager.socket_manager.register(sock)
        try:
            while True:
                message = await sock.recv()
                _logger.debug(f'received "{message}"')
                try:
                    message = json.loads(message)
                    await self.context_manager.run_cmd(message, sock)
                except ValueError:
                    _logger.error('message faulty')
                except Exception as e:
                    _logger.error(e)
        except websockets.ConnectionClosed:
            _logger.debug('socket disconnected')
        finally:
            await self.context_manager.socket_manager.unregister(sock)

    async def start(self):
        port = self.context_manager.config.ports['websocket']
        self.server = websockets.serve(
            self.websocket_client,
            '0.0.0.0',
            port,
            ssl=self.get_ssl_context(),
        )
        _logger.info(f'started websocket server on  port {port}')
        await self.server

    async def stop(self):
        self.server.ws_server.close()
        await self.server.ws_server.wait_closed()
