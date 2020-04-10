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


if __name__ == '__main__':
    config = Config()
    context = ContextManager(config)
    manager = TaskManager(context)

    if config.prod_mode:
        _logger.info('PROD mode active')
    else:
        manager.register('frontend')
        # manager.register('restarter') todo: unstable, rebuild...

    manager.register('webserver')
    manager.register('scheduler')

    try:
        manager.run()
    except KeyboardInterrupt:
        pass
