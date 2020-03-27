import asyncio
import importlib
import inspect
import logging

from sys import platform
from server.utils.module import Module

_logger = logging.getLogger('TaskManager')


class TaskManager(object):
    def __init__(self, context_manager):
        self.context_manager = context_manager
        self.context_manager.task_manager = self

        if platform == "win32":
            self.loop = asyncio.ProactorEventLoop()
        else:
            self.loop = asyncio.SelectorEventLoop()

        self.instances = {}
        self.tasks = {}
        self.modules = []

        asyncio.set_event_loop(self.loop)

    def register(self, name):

        if name not in self.modules:
            self.import_module(name)

    async def reimport_module(self, name):
        await self.stop(name)
        del self.instances[name]
        self.import_module(name)
        await self.start(name)

    def import_module(self, name):
        module_name = f'server.modules.{name}'

        module = importlib.import_module(module_name)
        if name in self.modules:
            importlib.reload(module)

        members = inspect.getmembers(module)
        subs = Module.__subclasses__()

        classes = [member for name, member in members if member in subs]
        if not classes:
            _logger.warning(f'{module_name} does not contain a Module')
            return

        if name not in self.modules:
            self.modules.append(name)

        self.instances[name] = classes[0](self.context_manager)

    async def _create_server_task(self, name, instance):
        task = asyncio.create_task(instance.start())
        self.tasks[name] = task

    async def start(self, name=None):
        if name:
            await self._start(name)
            return

        for name in self.instances:
            await self._start(name)

    async def stop(self, name=None):
        if name:
            await self._stop(name)
            return

        for name in self.tasks:
            await self._stop(name)

    async def _start(self, name):
        _logger.debug(f'starting {name}')

        instance = self.instances[name]
        await self._create_server_task(name, instance)

    async def _stop(self, name):
        _logger.debug(f'stopping {name}')

        await self.instances[name].stop()
        self.tasks[name].cancel()
        del self.tasks[name]

    async def restart(self, name=None):
        await self.stop(name)
        await self.start(name)

    def run(self):
        self.loop.run_until_complete(self.start())
        self.loop.run_forever()
