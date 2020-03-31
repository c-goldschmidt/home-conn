import importlib
import logging

import server
from server.chat.chat import ChatCMD
from server.database.db import Database
from server.management.socket_manager import SocketManager
from server.spotify.spotify import SpotifyCMD
from server.users.user_manager import UserManager

_logger = logging.getLogger('ContextManager')


class ContextManager:

    def __init__(self, config):
        self.config = config
        self.database = None
        self.task_manager = None
        self.socket_manager = None
        self.user_manager = None
        self.spotify = None
        self.chat = None
        self.cmd_instances = []
        self.first_load = True

        self.reload()

    def reload(self):
        if not self.first_load:
            importlib.reload(server)
            _logger.info('modules reloaded')

        self.database = Database()
        self.task_manager = None
        self.socket_manager = SocketManager(self)
        self.user_manager = UserManager(self)
        self.spotify = SpotifyCMD(self)
        self.chat = ChatCMD(self)

        self.cmd_instances = [
            self.spotify,
            self.chat,
            self.user_manager,
        ]
        self.first_load = False

    async def run_cmd(self, message, sender):
        if not self._valid(message):
            return

        handler = self._get_handler(message)
        if handler and self._check_user(sender, handler):
            await handler.run_cmd(message, sender)

        for cmd_class in self.cmd_instances:
            if message['type'] == cmd_class.TYPE:
                return

    def _get_handler(self, message):
        for cmd_class in self.cmd_instances:
            if message['type'] == cmd_class.TYPE:
                return cmd_class
        return None

    def _check_user(self, sender, handler):
        if not handler.requires_login:
            return True
        return self.user_manager.identify(sender) is not None

    def _valid(self, message):
        if not isinstance(message, dict):
            return False

        if not all([
            'type' in message,
            'cmd' in message,
            'payload' in message,
        ]):
            return False

        return True
