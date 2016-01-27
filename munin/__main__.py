"""

usage:
    __main__.py [options]
    __main__.py <configuration> [options]

options:
    --help, -h      print this doc
    --version, -v   print the version and quit
    --channel=STR   IRC channel to connect to

"""


import docopt
from munin.bot import Bot
from munin.info import VERSION
from munin.config import configuration
from munin.control import Control


if __name__ == '__main__':
    config = configuration(docopt_doc=__doc__)
    print(config)
    Control(Bot(config))
