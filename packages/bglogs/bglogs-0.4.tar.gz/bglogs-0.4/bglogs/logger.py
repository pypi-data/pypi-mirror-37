"""
Override logging base functions
"""


import inspect
import logging
from os import path

from bglogs import messages


_LOGGER = None


def _get_logger_parent(level=2):
    global _LOGGER

    curframe = inspect.currentframe()
    frame = inspect.getouterframes(curframe)[level].frame
    logger_name = frame.f_globals['__name__'].split('.')[0]
    # print('>>>', inspect.getframeinfo(frame))
    # print('<<<', frame.f_globals['__name__'])
    if logger_name == '__main__':  # replace main for
        logger_name = path.basename(frame.f_globals['__file__'])  # Do not split the extension to avoid collision with other loggers

    _LOGGER = logging.getLogger(logger_name)
    return _LOGGER


class StyleAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super(StyleAdapter, self).__init__(logger, extra or {})

    def log(self, level, msg, *args, exc_info=None, extra=None, stack_info=False, **kwargs):
        if self.isEnabledFor(level):
            msg, kw = self.process(msg, {})
            self.logger._log(level, messages.BraceMessage(msg, *args, **kwargs), (), **kw)


def get_logger(name=None, styled=True):
    logger = _LOGGER if name is None else logging.getLogger(name)
    if styled:
        return StyleAdapter(logger)
    else:
        return logger


def critical(msg, *args, **kwargs):
    _LOGGER.critical(messages.BraceMessage(msg, *args, **kwargs))


def error(msg, *args, **kwargs):
    _LOGGER.error(messages.BraceMessage(msg, *args, **kwargs))


def exception(msg, *args, exc_info=True, **kwargs):
    error(msg, *args, exc_info=exc_info, **kwargs)


def warning(msg, *args, **kwargs):
    _LOGGER.warning(messages.BraceMessage(msg, *args, **kwargs))


def info(msg, *args, **kwargs):
    _LOGGER.info(messages.BraceMessage(msg, *args, **kwargs))


def debug(msg, *args, **kwargs):
    _LOGGER.debug(messages.BraceMessage(msg, *args, **kwargs))
