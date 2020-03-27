import asyncio
import logging

from server.utils.module import Module
_logger = logging.getLogger('Module: Scheduler')


class SchedulerModule(Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.running = False
        self.shutdown_done = False

    async def fetch_status(self):
        await self.context_manager.spotify.update_playing_state()

    async def start(self):
        self.running = True

        while self.running:
            await self.fetch_status()
            await asyncio.sleep(15)
        self.shutdown_done = True

    async def stop(self):
        self.running = False

        while not self.shutdown_done:
            await asyncio.sleep(1)
