"""
Definition of the Configuration class.

This class manage the configurations values priority,
and provides an API for access the values.

"""

from enum import Enum
from collections import ChainMap
import json
import docopt


class AttrDict(ChainMap):
    """ChainMap having keys as attributes"""
    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError:
            return super().__getitem__(attr)


class Config(Enum):
    """All values in the config"""
    Server       = 'server'
    Port         = 'port'
    Channel      = 'channel'
    Nickname     = 'nickname'
    Realname     = 'realname'
    Password     = 'password'
    CheckTime    = 'check_time'
    Sudoers      = 'sudoers'
    Expressions  = 'expressions'
    Expressivity = 'expressivity'

    @staticmethod
    def keys():
        return set(c.value for c in Config)


DOCOPT_UNUSED_KEYS = {'--help', '--version', '<configuration>'}
DEFAULT_CONFIG = {
    Config.Server.value       : 'irc.freenode.net',
    Config.Port.value         : 6667,
    Config.Channel.value      : '#test_munin',
    Config.Nickname.value     : 'munin',
    Config.Realname.value     : 'munin',
    Config.Password.value     : '',
    Config.CheckTime.value    : 5,
    Config.Sudoers.value      : {},
    Config.Expressions.value  : {},
    Config.Expressivity.value : 0.0,
}


def extract_json(config_filename):
    """Return a dict representation of given file content"""
    with open(config_filename) as fd:
        return json.load(fd)


def configuration(docopt_doc=None, configfilename=None, configfile_parse=extract_json,
                  default_config=DEFAULT_CONFIG, version=None):
    """Return a dict-like object that describe the configuration"""
    clif_args, cnfg_args, dflt_args = {}, {}, {}
    if docopt_doc:
        docopt_args = docopt.docopt(docopt_doc, version=version)
        if not configfilename:
            configfilename = docopt_args.get('<configuration>', None)
        clif_args = {k.lstrip('-'): v for k, v in docopt_args.items()
                     if v is not None and k not in DOCOPT_UNUSED_KEYS}
        assert all(k in Config.keys() for k in clif_args.keys())
    if configfilename and configfile_parse:
        cnfg_args = configfile_parse(configfilename)
    if default_config:
        dflt_args = default_config
    config = ChainMap({}, clif_args, cnfg_args, dflt_args)
    assert all(k in Config.keys() for k in config)
    return AttrDict(config)
