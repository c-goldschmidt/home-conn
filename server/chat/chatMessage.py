import re

rx_mention = re.compile(r'@(?P<username>[a-z0-9]+)')


class ChatMessage:
    def __init__(self, id, sender_id, message, timestamp, context_manager):
        self.context_manager = context_manager
        self.user_manager = context_manager.user_manager

        self.id = id
        self.sender_id = sender_id
        self.message = message
        self.timestamp = timestamp

        self.sender = None
        self.mentions = None

        self.parse()

    def parse(self):
        self.sender = self.user_manager.get_user(self.sender_id)

        mention_names = {}
        for result in rx_mention.finditer(self.message):
            name = result.group('username').lower()
            if name not in mention_names:
                mention_names[name] = {
                    'replace': result.group('username'),
                    'user': None,
                }

        for user in self.user_manager.user_list:
            if user.lc_name in mention_names:
                mention_names[user.lc_name]['user'] = user

        self.mentions = [item['user'] for item in mention_names.values()]
        for replace_dict in mention_names.values():
            user = replace_dict['user']

            if not user:
                continue

            self.message = self.message.replace(
                f'@{replace_dict["replace"]}',
                f'[color=#ccffff][mention={user.id}]@{user.name}[/mention][/color]',
            )

    def to_dict(self):
        return {
            'message': self.message,
            'sender_name': self.sender.name,
            'timestamp': self.timestamp,
            'mentions': [user.to_public_dict() for user in self.mentions],
        }