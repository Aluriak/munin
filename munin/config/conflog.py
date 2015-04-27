# -*- coding: utf-8 -*-
#########################
#       CONFLOG         #
#########################
"""
Definitions of logging.
"""

#########################
# IMPORTS               #
#########################
import logging
from logging.handlers import RotatingFileHandler


FILENAME_LOG = 'logs/munin.log'
LOGGER_NAME  = 'munin'
LOGGER       = logging.getLogger(LOGGER_NAME)


#########################
# INIT LOGGING          #
#########################
LOGGER.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s :: %(levelname)s :: %(message)s'
)

# create a handler to file
file_handler = RotatingFileHandler(
    FILENAME_LOG, # filename
    'a', 1000000, 1 # append, 1 Mo, 1 backup
)
# and define its level and formatter
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# add handlers to LOGGER
for handler in (file_handler,):
    LOGGER.addHandler(handler)
