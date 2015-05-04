# -*- coding: utf-8 -*-
#########################
#       CONTROL         #
#########################
"""
Define the controller of the Bot itself.

The controller provide a full command line interface for administration:
    - dynamic plugins
    - IRC interactions
    - sudoers management
"""


#########################
# IMPORTS               #
#########################
import threading
import cmd
import re
import munin.config as config
# integrated command line
from prompt_toolkit.contrib.shortcuts import get_input
from prompt_toolkit.contrib.regular_languages.compiler import compile as pt_compile


#########################
# PRE-DECLARATIONS      #
#########################
LOGGER = config.logger()
# list of reusable subcommands names
COMMAND_PLUGINS_ADD = ('add', 'a', 'activate')
COMMAND_PLUGINS_DEL = ('deactivate', 'del', 'd', 'rm', 'r')
COMMAND_PLUGINS_LS  = ('ls', 'l')
COMMAND_PLUGINS_PRT = ('p', 'print')
COMMAND_SUDO_ADD    = ('a', 'add')
COMMAND_SUDO_DEL    = ('d', 'del', 'rm')
# all commands, subcommands and other regex in a main dict
COMMAND_NAMES = {
    'quit'    : ('q', 'quit', ':q', 'exit'),
    'sudo'    : ('sudo', 'sudoers', 'sd'),
    'plugins' : ('plugins', 'plugin', 'pg', 'pl', 'plg'),
    'irc'     : ('irc', 'lastwords', 'words', 'last', 'lw', 'w', 'wl'),
    'say'     : ('say',),
    'subsudo' : COMMAND_SUDO_ADD + COMMAND_SUDO_DEL,
    'subpgarg': COMMAND_PLUGINS_ADD + COMMAND_PLUGINS_DEL,
    'subpgnoa': COMMAND_PLUGINS_PRT + COMMAND_PLUGINS_LS,
    'args'    : ('.*',),
}
# printings values
PRINTINGS_PLUGINS_MAX_WIDTH = 20
DEFAULT_INTRO  = 'Welcome to the munin shell. Type help or ? to list commands.\n'
DEFAULT_PROMPT = '?>'


# COMMANDS
def commands_grammar():
    """Return a grammar for COMMAND_NAMES values."""
    def cmd2reg(cmd, subcmd=None, args=None):
        """layout automatization"""
        return (
            '(\s*  (?P<cmd>(' + '|'.join(COMMAND_NAMES[cmd]) + '))'
            + ('' if subcmd is None
               else ('\s+  (?P<subcmd>('+'|'.join(COMMAND_NAMES[subcmd]) + '))   \s*  '))
            + ('' if args   is None
               else ('\s+  (?P<args>('  +'|'.join(COMMAND_NAMES[args  ]) + '))   \s*  '))
            + ') |\n'
        )
    # get grammar, log it and return it
    grammar = (
          cmd2reg('sudo'   , 'subsudo' , 'args')
        + cmd2reg('quit'   , None      , None  )
        + cmd2reg('plugins', 'subpgnoa', None  )
        + cmd2reg('plugins', 'subpgarg', 'args')
        + cmd2reg('irc'    , None      , 'args')
        + cmd2reg('say'    , None      , 'args')
    )
    LOGGER.debug('GRAMMAR:\n' + grammar)
    return pt_compile(grammar)


#########################
# CONTROL CLASS         #
#########################
class Control():
    """
    Control a Bot, as defined in bot.py file.
    Allow user to type its commands and use Control instance
    as an IRC client.
    """


# CONSTRUCTOR #################################################################
    def __init__(self, bot, prompt=DEFAULT_PROMPT, intro=DEFAULT_INTRO):
        self.bot, self.finished = bot, False

        # launch bot as thread
        self.bot_thread = threading.Thread(target=self.bot.start)
        self.bot_thread.start()

        # Initial plugins
        available_plugins = tuple(
            config.import_plugins()
        )

        # Add whitelisted plugins automatically # TODO
        for f in available_plugins:
            self.bot.add_plugin(f())
            LOGGER.info('PLUGIN LOADED: ' + f.__name__)

        # main loop control
        LOGGER.info('Connected !')
        print(intro, end='')
        grammar = commands_grammar()
        while True:
            text  = get_input(prompt)
            match = grammar.match(text)
            if match is not None:
                values = match.variables()
                cmd    = values.get('cmd')
                subcmd = values.get('subcmd')
                args   = values.get('args')
                LOGGER.debug('LINE:' + str(cmd) + str(subcmd) + str(args))
                if cmd in COMMAND_NAMES['sudo']:
                    self.__sudo(subcmd, args)
                elif cmd in COMMAND_NAMES['plugins']:
                    self.__plugins(subcmd, args)
                elif cmd in COMMAND_NAMES['quit']:
                    self.__disconnect()
                elif cmd in COMMAND_NAMES['say']:
                    self.__say(args)
                elif cmd in COMMAND_NAMES['irc']:
                    self.__last_words(args)
                # elif cmd in ('', ''):
                    # self.
            else:
                print('not a valid command')

        # try:
            # print("?>", end='')
            # cmd = input('')
            # while not self.finished:
                # self.finished = not self.bot.is_connected()
                # self.do_command(cmd)
                # if not self.finished:
                    # print("?>", end='')
                    # cmd = input('')
        # except KeyboardInterrupt:
            # self.bot.disconnect()
        # except EOFError:
            # self.bot.disconnect()

        LOGGER.info('Disconnected !')
        # finalize all treatments
        self.bot_thread.join()


# PUBLIC METHODS ##############################################################
# PRIVATE METHODS #############################################################
    def __sudo(self, subcmd, arg):
        """add asked sudoer to bot sudoers list"""
        if subcmd in COMMAND_SUDO_ADD:
            print('SUDOERS: adding', arg, 'is necessary, but actually not performed')
        else:
            print('SUDOERS: removing', arg, 'is necessary, but actually not performed')
        LOGGER.debug(arg)
        LOGGER.debug('not implemented !')
        print('OK !')
        #self.bot.add_sudoer(arg)

    def __disconnect(self):
        """disconnect and quit all"""
        self.finished = True
        self.bot.disconnect()

    def __say(self, regex_result):
        """print message in canal"""
        self.bot.send_message(regex_result[0])
        LOGGER.debug('Said:' + str(regex_result[0]))

    def __plugins(self, subcmd, values):
        """management of plugins"""
        error_code = {
            'name'  : 'need a valid plugin name',
            'id'    : 'need a valid plugin index',
        }
        error = None

        # listing
        if subcmd in COMMAND_PLUGINS_LS:
            assert(values is None)
            # each plugin will be shown with a [ACTIVATED] flag
            #  if already present of munin
            plugins = ((
                        (p.__name__[:PRINTINGS_PLUGINS_MAX_WIDTH]
                         + ' ' * (PRINTINGS_PLUGINS_MAX_WIDTH
                                  - len(p.__name__[:PRINTINGS_PLUGINS_MAX_WIDTH])
                                 )
                         + '\t[ACTIVATED]'
                        )
                        if p in self.bot else p.__name__
                       )
                       for p in config.import_plugins()
                      )
            print('\n'.join(plugins))
        # printing
        if subcmd in COMMAND_PLUGINS_PRT:
            assert(values is None)
            for fn in (str(f) for f in self.bot.plugins):
                print(str(fn))
        # activation
        elif subcmd in COMMAND_PLUGINS_ADD:
            assert(values is not None)
            if len(values) > 0:
                for name in values:
                    clss = config.import_plugin(name)
                    for cls in clss:
                        self.bot.add_plugin(cls())
            else:
                error = 'name'
        # deactivation
        elif subcmd in COMMAND_PLUGINS_DEL:
            assert(values is not None)
            if len(values) > 0:
                try:
                    for idx in (int(_) for _ in values):
                        if not self.bot.rmv_index(idx):
                            print(str(idx) + ' not found !')
                except ValueError:
                    error = 'id'
            else:
                error = 'id'
        # error output
        if error is not None:
            print('ERROR:', error_code[error])


    def __last_words(self, args):
        """Show last words on channel"""
        args = int(args)
        if args > 0:
            raise NotImplementedError
        else:
            print('ERROR:', args, 'is not a valid number of message to display')


# PREDICATS ###################################################################
# ACCESSORS ###################################################################
# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



