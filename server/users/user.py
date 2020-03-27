
class User:

    def __init__(self, name=None, lc_name=None, user_id=None, uuid=None, socket=None):
        self.name = name
        self.lc_name = lc_name
        self.id = user_id
        self.uuid = uuid
        self.socket = socket

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'token': self.uuid,
        }

    def to_public_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
