import logging

from server.chat.chatMessage import ChatMessage
from server.database.queries import SQL_SELECT_ALL_MESSAGES, SQL_CREATE_MESSAGE, SQL_SELECT_MESSAGE
from server.utils.base_cmd import BaseCmd

_logger = logging.getLogger('ChatCMD')


class ChatCMD(BaseCmd):
    TYPE = 'chat'

    def __init__(self, context_manager):
        super().__init__(context_manager)
        self.db = self.context_manager.database
        self.messages = []
        self.fetch()

    async def run_cmd(self, message, sender):
        if message['cmd'] == 'request_log':
            await self.handle_log_request(message, sender)
        if message['cmd'] == 'send':
            await self.handle_send_message(message, sender)

    async def handle_log_request(self, message, sender):
        max_entires = message['payload'].get('max_entires')
        messages = self.messages[-max_entires:len(self.messages)]

        await self.context_manager.socket_manager.send_to_socket(sender, {
            'type': 'chat_backlog',
            'payload': [message.to_dict() for message in messages],
        })

    async def handle_send_message(self, message, sender):
        sending_user = self.context_manager.user_manager.identify(sender)
        if not sending_user:
            return await self.context_manager.socket_manager.send_to_socket(sender, {
                'type': 'chat_send_result',
                'payload': {'success': False, 'error': 'only users can do this'},
            })

        message = self._create(message['payload'], sending_user.id)
        if not message:
            return await self.context_manager.socket_manager.send_to_socket(sender, {
                'type': 'chat_send_result',
                'payload': {'success': False, 'error': 'DB error'},
            })

        return await self.context_manager.user_manager.send_to_all_users({
            'type': 'chat_message',
            'payload': message.to_dict(),
        })

    def _create(self, message, sender_id):
        message_id = self.db.execute(SQL_CREATE_MESSAGE, {
            'sender_id': sender_id,
            'message': message
        }, commit=True)

        if not message_id:
            return None

        message_id, sender_id, message, timestamp = self.db.execute_fetch_one(
            SQL_SELECT_MESSAGE, {'id': message_id}
        )
        result_message = ChatMessage(message_id, sender_id, message, timestamp, self.context_manager)
        self.messages.append(result_message)
        return result_message

    def fetch(self):
        results = self.db.execute_fetch_all(SQL_SELECT_ALL_MESSAGES)
        self.messages = []
        for message_id, sender_id, message, timestamp in results:
            self.messages.append(ChatMessage(
                message_id, sender_id, message, timestamp, self.context_manager,
            ))

        _logger.info(f'loaded {len(self.messages)} chat messages')