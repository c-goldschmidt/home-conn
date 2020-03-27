import asyncio


class Module(object):
    def __init__(self, context_manager):

        self.context_manager = context_manager
        self.loop = asyncio.get_event_loop()

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
