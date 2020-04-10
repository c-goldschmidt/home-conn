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
        self.last_calls = {}

        self.configs = {
            'status': {
                'callback': self.fetch_status,
                'interval': self.context_manager.config.spotify.int('song_update_delay', 15),
            },
            'devices': {
                'callback': self.fetch_devices,
                'interval': self.context_manager.config.spotify.int('device_update_delay', 30),
            }
        }
        self.config_keys = list(self.configs.keys())

    async def fetch_status(self):
        await self.context_manager.spotify.update_playing_state()

    async def fetch_devices(self):
        await self.context_manager.spotify.update_devices()

    async def run_task(self, label, callback, delay):
        if label not in self.last_calls:
            self.last_calls[label] = time.time()

        last_call = self.last_calls[label]
        if time.time() - last_call > delay:
            await callback()
            self.last_calls[label] = time.time()

    async def run_tasks(self):
        coros = []
        for key, config in self.configs.items():
            coros.append(self.run_task(key, config['callback'], config['interval']))

        exceptions = await asyncio.gather(*coros, loop=self.loop, return_exceptions=True)
        for index, ex in enumerate(exceptions):
            if not ex:
                continue
            _logger.error(f'{self.config_keys[index]}: {ex}')

    async def start(self):
        self.running = True

        _logger.info('starting scheduler')
        while self.running:
            await self.run_tasks()
            await asyncio.sleep(1)
        self.shutdown_done = True

    async def stop(self):
        self.running = False

        while not self.shutdown_done:
            await asyncio.sleep(1)
