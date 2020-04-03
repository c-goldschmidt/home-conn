import asyncio
import logging

from modulefinder import ModuleFinder

from server.utils.constants import SERVER_PATH
from server.utils.module import Module

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

_logger = logging.getLogger('Module: Watchdog')


class EventHandler(FileSystemEventHandler):

    def __init__(self, context_manager, queue):
        self.task_manager = context_manager.task_manager
        self.queue = queue

    def on_modified(self, event):
        if not event.src_path.endswith('.py'):
            return

        print(f'modules using {event.src_path}')
        finder = ModuleFinder()
        finder.load_file(event.src_path)
        for name, mod in finder.modules.items():
            print(name)
            print(mod)


class WatchdogModule(Module):
    KEEP_RUNNING = ['frontend', 'restarter']

    def __init__(self, *args):
        super().__init__(*args)
        self.task_manager = self.context_manager.task_manager
        self.running = False
        self.shutdown_done = False
        self.restart_queue = []

    async def restart_modules(self):
        for module in self.task_manager.modules:
            if module in self.KEEP_RUNNING:
                continue

            await self.task_manager.reimport_module(module)

    async def check_queue(self):
        if self.restart_queue:
            await self.restart_modules()
        self.restart_queue[:] = []

    async def start(self):
        self.running = True

        event_handler = EventHandler(self.context_manager, self.restart_queue)
        observer = Observer()
        observer.schedule(event_handler, SERVER_PATH, recursive=True)
        observer.start()

        while self.running:
            await self.check_queue()
            await asyncio.sleep(5)

        print('stop checking now')
        self.shutdown_done = True

    async def stop(self):
        self.running = False
        while not self.shutdown_done:
            await asyncio.sleep(1)

