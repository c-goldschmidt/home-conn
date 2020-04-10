import logging
import os

# paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FE_PATH = os.path.join(BASE_PATH, 'frontend')
STATIC_DIR = os.path.join(FE_PATH, 'dist')
SERVER_PATH = os.path.join(BASE_PATH, 'server')
CACHE_PATH = os.path.join(BASE_PATH, 'cache')

LIST = []

# logging
LOG_LEVEL = logging.INFO
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}
