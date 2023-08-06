import copy
import logging
from logging import config as loggingconfig

from bglogs import logger as loggermod


BGCONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'bgfmt': {
            '()': 'bglogs.format.BGFmt'
        },
    },
    'filters': {
        'info': {
            '()': 'bglogs.filter.InfoFilter'
        }
    },
    'handlers': {
        'bgout': {
            'class': 'logging.StreamHandler',
            'formatter': 'bgfmt',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
            'filters': ['info']
        },
        'bgerr': {
            'class': 'logging.StreamHandler',
            'formatter': 'bgfmt',
            'level': 'WARNING',
            'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {},
}


def init_config():
    logger = loggermod._get_logger_parent(level=8)

    conf = copy.deepcopy(BGCONF)
    # Configure application logger
    conf['loggers'][logger.name] = {
        'level': logging.DEBUG
    }
    # Configure root logger
    conf['root'] = {
        'level': 'WARNING',
        'handlers': ['bgout', 'bgerr']
    }

    loggingconfig.dictConfig(conf)


def configure(name=None, debug=False):
    if name is None:
        logger = loggermod._get_logger_parent(level=2)
    else:
        logger = loggermod.get_logger(name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
