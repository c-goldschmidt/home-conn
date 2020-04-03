import hashlib
import logging
import sqlite3
import uuid

from server.database.queries import SQL_CREATE_USER, SQL_GET_USER, SQL_SET_PASSWORD, SQL_GET_USERS
from server.users.user import User
from server.utils.base_cmd import BaseCmd

_logger = logging.getLogger('UserManager')


class UserManager(BaseCmd):
    TYPE = 'user'
    requires_login = False

    def __init__(self, context_manager):
        super().__init__(context_manager)
        self.db = context_manager.database
        self.socket_manager = context_manager.socket_manager

        self.user_list = []
        self.fetch()

    def identify(self, socket):
        for user in self.user_list:
            if user.socket is not None and user.socket == socket:
                return user
        return None

    def get_user(self, user_id):
        users = [user for user in self.user_list if user.id == user_id]
        return users[0] if users else None

    @property
    def has_logged_in(self):
        users = [user for user in self.user_list if user.socket]
        return len(users) > 0

    async def send_to_all_users(self, message):
        for user in self.user_list:
            if user.socket:
                await self.socket_manager.send_to_socket(user.socket, message)

    async def run_cmd(self, message, sender):
        if message['cmd'] == 'login' or message['cmd'] == 'token_login':
            await self._login_socket(message, sender)
        if message['cmd'] == 'fetch_users':
            await self._send_user_list(sender)

    async def _send_user_list(self, socket):
        if not self.identify(socket):
            await self.socket_manager.send_to_socket(socket, {
                'type': 'user_result',
                'payload': [],
            })

        await self.socket_manager.send_to_socket(socket, {
            'type': 'user_result',
            'payload': [user.to_public_dict() for user in self.user_list],
        })

    async def _login_socket(self, message, sender, retry=True):
        logged_in = self.login(
            message['payload'].get('username'),
            message['payload'].get('password'),
            message['payload'].get('token'),
        )

        if logged_in:
            _logger.info(f'user {logged_in.name} logged in')
            logged_in.socket = sender
            return await self._respond_login(sender, True, logged_in)
        elif retry and 'token' not in message['payload'] and self.create_user(
            message['payload']['username'],
            message['payload']['password']
        ):
            return await self._login_socket(message, sender, False)
        elif retry and 'token' not in message['payload']:
            return await self._respond_login(sender, False, 'user already exists with a different password')

        await self._respond_login(sender, False, 'password or token does not match')

    async def _respond_login(self, sender, success, message):
        payload = {'success': success}
        if success:
            payload['user'] = message.to_dict()
        else:
            payload['message'] = message

        await self.socket_manager.send_to_socket(sender, {
            'type': 'login_result',
            'payload': payload,
        })

    def fetch(self):
        users = self.db.execute_fetch_all(SQL_GET_USERS)

        new_list = []
        for user_id, name, lc_name, uuid in users:
            ex_user = self.get_user(user_id)
            new_list.append(User(
                user_id=user_id,
                name=name,
                lc_name=lc_name,
                uuid=uuid,
                socket=ex_user.socket if ex_user else None
            ))
        self.user_list = new_list

        _logger.debug(f'{len(self.user_list)} Users loaded')

    def create_user(self, name, password):
        if not self.context_manager.config.server.bool('allow_account_creation'):
            _logger.warning('someone tried to signup, but allow_account_creation is disabled')
            return False

        params = {
            'name': name,
            'lc_name': name.lower(),
            'password': hashlib.sha512(password.encode('utf-8')).hexdigest(),
            'uuid': str(uuid.uuid5(uuid.NAMESPACE_URL, name)),
        }

        with self.db.cursor() as cur:
            try:
                cur.execute(SQL_CREATE_USER, params)
                self.db.commit()
                _logger.info(f'created new user "{name}"')
            except sqlite3.IntegrityError:
                _logger.warning(f'could not create user "{name}" (already exists)')
                return False

        self.fetch()
        return True

    def login(self, name, password=None, user_uuid=None):
        params = {
            'name': name,
            'password': hashlib.sha512(password.encode('utf-8')).hexdigest() if password else '_NONE_',
            'uuid': user_uuid or '_NONE_',
        }

        with self.db.cursor() as cur:
            cur.execute(SQL_GET_USER, params)
            result = cur.fetchone()
            if not result:
                _logger.warning(f'login failed: {params}')
                return None

        return self.get_user(result[0])

    def set_password(self, name, new_pass, old_pass):
        params = {
            'name': name,
            'new_pass': hashlib.sha512(new_pass.encode('utf-8')).hexdigest(),
            'old_pass': hashlib.sha512(old_pass.encode('utf-8')).hexdigest(),
        }

        with self.db.cursor() as cur:
            cur.execute(SQL_SET_PASSWORD, params)
            self.db.commit()

            if cur.rowcount > 0:
                return True

        return False
