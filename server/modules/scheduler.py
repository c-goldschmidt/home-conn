import asyncio
import logging
import time
from collections import defaultdict

from server.utils.module import Module
_logger = logging.getLogger('Module: Scheduler')


class SchedulerModule(Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.running = False
        self.shutdown_done = False
        self.last_calls = defaultdict(time.time)

    async def fetch_status(self):
        await self.context_manager.spotify.update_playing_state()

    async def fetch_devices(self):
        await self.context_manager.spotify.update_devices()

    async def run_loop(self, label, callback, delay):
        last_call = self.last_calls[label]
        if time.time() - last_call > delay:
            await callback()
            self.last_calls[label] = time.time()

    async def start(self):
        self.running = True

        while self.running:
            await asyncio.gather(
                self.run_loop('status', self.fetch_status, 15),
                self.run_loop('devices', self.fetch_devices, 30),
            )
            await asyncio.sleep(1)
        self.shutdown_done = True

    async def stop(self):
        self.running = False

        while not self.shutdown_done:
            await asyncio.sleep(1)
