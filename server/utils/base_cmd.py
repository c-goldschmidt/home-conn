class BaseCmd:
    TYPE = None
    requires_login = True

    def __init__(self, context_manager):
        self.context_manager = context_manager

    async def run_cmd(self, message, sender):
        raise NotImplementedError()
