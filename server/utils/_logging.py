import logging
import os
import _locale

from server.utils.constants import RESET_SEQ, BOLD_SEQ, COLORS, COLOR_SEQ, GREEN

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


def formatter_message(message, use_color=True):
    if ColoredLogger.LOG_LEVEL == logging.DEBUG:
        message += ' ($BOLD%(filename)s$RESET:%(lineno)d)'

    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")

    len_modifier = 12 if use_color else 0
    message = message.replace('$MAX_MSG_LENGTH', str(ColoredFormatter.MAX_MSG_LENGTH + 2 + len_modifier))
    message = message.replace('$MAX_LVL_LENGTH', str(ColoredFormatter.MAX_LVL_LENGTH + len_modifier))

    return message


class ColoredFormatter(logging.Formatter):
    MAX_MSG_LENGTH = 1
    MAX_LVL_LENGTH = 8   # CRITICAL

    def __init__(self, fmt, use_color=True):
        logging.Formatter.__init__(self, fmt)
        self.fmt = fmt
        self.use_color = use_color

    def _color(self, color):
        return COLOR_SEQ % (30 + color)

    def format(self, record):
        fmt = formatter_message(self.fmt, self.use_color)

        record.message = record.getMessage()
        levelname = record.levelname
        if self.use_color:
            record.name = f'[{self._color(GREEN)}{record.name}{RESET_SEQ}]'
            if levelname in COLORS:
                levelname_color = f'{self._color(COLORS[levelname])}{levelname}{RESET_SEQ}'
                record.levelname = f'[{levelname_color}]'
        else:
            record.name = f'[{record.name}]'
            record.levelname = f'[{record.levelname}]'

        return fmt % record.__dict__


class ColoredLogger(logging.Logger):
    FORMAT = "%(levelname)-$MAX_LVL_LENGTHs%(name)-$MAX_MSG_LENGTHs > %(message)s"
    LOG_LEVEL = logging.INFO

    def __init__(self, name):
        ColoredFormatter.MAX_MSG_LENGTH = max(ColoredFormatter.MAX_MSG_LENGTH, len(name))
        logging.Logger.__init__(self, name, self.LOG_LEVEL)

        color_formatter = ColoredFormatter(self.FORMAT, os.name == 'nt')

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.propagate = False
        self.addHandler(console)


def activate(log_level=logging.INFO):
    ColoredLogger.LOG_LEVEL = log_level
    logging.setLoggerClass(ColoredLogger)
