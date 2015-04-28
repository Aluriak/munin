# -*- coding: utf-8 -*-
#########################
#       CONFIG          #
#########################
"""
Definitions of default configurations, mainly about logging.
"""

#########################
# IMPORTS               #
#########################
import importlib
import itertools
import logging
import glob
import os

from logging.handlers import RotatingFileHandler
from munin.plugin     import Plugin



#########################
# PRE-DECLARATIONS      #
#########################
PKG_NAME        = 'munin'
DIR_PLUGINS     = 'plugins'


#########################
# LOGGING ACCESS        #
#########################
def logger(name=''):
    """Return logger of munin

    If name is provided, it will be registered like a submodule of munin.
    Adapted for Plugins.
    """
    import munin.config.conflog as conflog
    logger_name = conflog.LOGGER_NAME
    if len(name) > 0:
        return logging.getLogger(logger_name + '.' + name)
    else:
        return logging.getLogger(logger_name)





#########################
# IMPORT USER CLASSES   #
#########################
def import_functionnalities():
    """Import all modules in subdirectory of munin functionnalities directory.

    Return a generator of classes.
    """
    def class_check(cls):
        return (
            issubclass(cls.__class__, type) and # its a class !
            issubclass(cls, Functionnality) and # its a functionnality
            cls is not Functionnality           # but not Functionnality itself
        )
    # open python modules in user classes directory
    # ex: 'A/B/C.py' -> 'A.B.C'
    modules = (f.replace('/', '.').rstrip('.py')
               for f in glob.glob('munin/functionnalities/*/'+'*.py')
               if '__init__' not in f
              )
    # collect all expected classes in userclasses list
    classes = []
    for module in modules:
        # import user module
        module = importlib.import_module(module, package=PKG_NAME)
        # collect expected classes
        attributes = (module.__getattribute__(_) for _ in module.__dir__())
        attributes = tuple(_ for _ in attributes if class_check(_))
        classes.append(attributes)

    return itertools.chain(*classes)

