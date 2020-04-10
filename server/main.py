from server.utils._logging import activate

import argparse
import logging

_logger = logging.getLogger('MAIN')


def get_args():
    parser = argparse.ArgumentParser(description='MainEntrypoint')
    parser.add_argument('--config', type=str, default='config.ini')
    parser.add_argument('--loglevel', type=int, default=logging.INFO)
    return parser.parse_args()


def setup():
    args = get_args()
    activate()

    from server.utils.config import Config
    from server.management.task_manager import TaskManager
    from server.management.context_manager import ContextManager

    config = Config(args.config)
    context = ContextManager(config)
    manager = TaskManager(context)

    return config, manager


if __name__ == '__main__':
    config, manager = setup()

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
