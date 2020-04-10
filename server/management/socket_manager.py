import json
import logging

_logger = logging.getLogger('SocketManager')


class SocketManager(object):
    def __init__(self, context_manager):
        self.context_manager = context_manager
        self.sockets = set()

    async def register(self, socket):
        _logger.debug('registered new socket')
        self.sockets.add(socket)

    def identify(self, socket):
        return self.context_manager.user_manager.identify(socket)

    async def unregister(self, socket):
        _logger.debug('unregistered socket')

        user = self.identify(socket)
        if user:
            _logger.debug(f'user {user.name} logged out')
            user.socket = None

        self.sockets.remove(socket)

    async def send_to_all(self, message):
        _logger.debug(f'send_to_all: "{message}"')
        for socket in self.sockets:
            await self.send_to_socket(socket, message)

    @staticmethod
    async def send_to_socket(sock, message):
        _logger.debug(f'send_to_socket: "{message}"')
        await sock.send_str(json.dumps(message))
