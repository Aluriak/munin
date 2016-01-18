# -*- coding: utf-8 -*-
#########################
#       CONFIG          #
#########################
"""
Definitions of default configurations,
mainly about logging and plugin importing.
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
from munin.info       import PKG_NAME


PKG_NAME        = 'munin'
DIR_PLUGINS     = 'plugins'


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


def plugin_class_check(cls):
    """Return True iff given cls is a valid plugin class"""
    return (
        issubclass(cls.__class__, type) and # its a class !
        issubclass(cls, Plugin) and # its a plugin
        cls is not Plugin           # but not Plugin itself
    )


def import_plugins():
    """Import all modules in subdirectory of munin plugins directory.

    Return a generator of classes.
    """
    # collect all expected classes in userclasses list
    classes = (import_plugin(module) for module in list_plugins())
    return itertools.chain(*classes)


def import_plugin(name, path=None, package=PKG_NAME):
    """Return generator of plugin classes in module of given name.

    Return empty generator if any ImportError raised.
    """
    # get full path
    if path is None:
        path = name
    else:
        path += '/' + name
    # importing
    try:
        # import user module
        module = importlib.import_module(path, package=package)
        # collect expected classes
        classes = (module.__getattribute__(_) for _ in module.__dir__())
        classes = (_ for _ in classes if plugin_class_check(_))
    except ImportError:
        classes = tuple()
    return classes


def list_plugins():
    """Return generator of plugin names that are detected and importables."""
    # open python modules in user classes directory
    # ex: 'A/B/C.py' -> 'A.B.C'
    return (f.rstrip('.py').replace('/', '.')
            for f in glob.glob(DIR_PLUGINS + '/*.py')
            if not f.startswith('_')
           )


