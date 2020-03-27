import os

from server.utils._logging import activate; activate()

import argparse
import logging
import subprocess

from server.utils.constants import FE_PATH
from server.utils.config import Config
from server.management.task_manager import TaskManager
from server.management.context_manager import ContextManager

_logger = logging.getLogger('MAIN')


def get_args():
    parser = argparse.ArgumentParser(description='MainEntrypoint')


def compile_frontend(config):
    prefix = config.url_prefix

    if not os.path.isdir(os.path.join(FE_PATH, 'node_modules')):
        print('installing dependencies')
        subprocess.run(
            ['npm', 'install', '--prod'],
            shell=True,
            cwd=FE_PATH,
        )

    if not os.path.isdir(os.path.join(FE_PATH, 'dist')):
        print('compiling frontend')
        subprocess.run(
            ['npm', 'run', 'build', '--', '--prod', f'--deploy-url={prefix}/static/', f'--base-href={prefix}/',  '--aot'],
            shell=True,
            cwd=FE_PATH,
        )


if __name__ == '__main__':
    config = Config()
    context = ContextManager(config)
    manager = TaskManager(context)

    if config.prod_mode:
        _logger.info('PROD mode active')
        compile_frontend(config)
    else:
        manager.register('frontend')
        manager.register('restarter')

    manager.register('websocket')
    manager.register('webserver')
    manager.register('scheduler')

    try:
        manager.run()
    except KeyboardInterrupt:
        pass
