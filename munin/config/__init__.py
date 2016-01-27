from .config import *
from .importing import *
from . import conflog




def logger(name=''):
    """Return logger of munin

    If name is provided, it will be registered like a submodule of munin.
    Adapted for Plugins.
    """
    logger_name = conflog.LOGGER_NAME
    if len(name) > 0:
        return logging.getLogger(logger_name + '.' + name)
    else:
        return logging.getLogger(logger_name)
