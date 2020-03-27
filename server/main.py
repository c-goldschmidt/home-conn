import argparse
import logging

from server.utils._logging import activate; activate()

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

    manager.register('websocket')
    manager.register('webserver')
    manager.register('scheduler')

    if config.prod_mode:
        _logger.info('PROD mode active')
    else:
        manager.register('frontend')
        manager.register('restarter')

    try:
        manager.run()
    except KeyboardInterrupt:
        pass
