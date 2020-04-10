import asyncio
import logging

from server.utils.constants import FE_PATH
from server.utils.module import Module
from server.utils.utils import get_ip

_logger = logging.getLogger('Module: Frontend')


class FrontendModule(Module):

    def __init__(self, *args):
        super().__init__(*args)
        self.process = None
        self.port = self.context_manager.config.server.int('dev_port')

    async def _read_stream(self, stream):
        while True:
            try:
                line = await stream.readline()
            except ValueError as e:
                _logger.error(e)
                break

            data = line.decode()
            _logger.debug(data)
            if data:
                if 'Compiled successfully' in data:
                    _logger.info(f'started frontend server on {get_ip()}:{self.port}')
                if 'Compiling...' in data:
                    _logger.info('frontend recompiling')
                if 'ERR' in data:
                    _logger.error(data)
            else:
                break

    async def start(self):
        cmd = f'npm run start -- --host 0.0.0.0 --port {self.port}'

        self.process = await asyncio.create_subprocess_shell(
            cmd,
            cwd=FE_PATH,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            loop=self.loop,
        )

        await asyncio.wait([
            self._read_stream(self.process.stdout),
            self._read_stream(self.process.stderr),
        ])

        await self.process.communicate()

    async def stop(self):
        try:
            self.process.terminate()
            await self.process.wait()
        except ProcessLookupError:
            _logger.warning('Process already terminated')
