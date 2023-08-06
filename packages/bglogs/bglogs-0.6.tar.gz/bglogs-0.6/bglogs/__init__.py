__version__ = '0.6'
from .logger import critical, error, warning, info, debug
from .configuration import init_config as __init_config, configure
from .logger import get_logger
__init_config()