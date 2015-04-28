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
import re

import munin.config as config



#########################
# PRE-DECLARATIONS      #
#########################
LOGGER          = config.logger()
RGX_SUDOERS_ADD = re.compile(r"\s*sudoers\s+add\s*([a-zA-Z0-9_]*)\s*")
RGX_DISCONNECT  = re.compile(r"\s*(quit|:q)\s*")
RGX_SPEAK       = re.compile(r"\s*say\s(.*)")
RGX_PLUGINS     = re.compile(r"\s*(plugins?|pl?g)\s(.*)")
RGX_LAST_WORDS  = re.compile(r"\s*irc\s(.*)")

# PRINTINGS
PRINTINGS_PLUGINS_MAX_WIDTH = 20



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
    def __init__(self, bot):
        self.bot, self.finished = bot, False
        self.commands = {
            RGX_SUDOERS_ADD : self.__bot_add_sudoer,
            RGX_DISCONNECT  : self.__bot_disconnect,
            RGX_SPEAK       : self.__bot_speak,
            RGX_PLUGINS     : self.__plugins,
            RGX_LAST_WORDS  : self.__last_words,
        }

        # launch bot as thread
        self.bot_thread = threading.Thread(target=self.bot.start)
        self.bot_thread.start()

        # Initial plugins
        self.available_plugins = tuple(
            config.import_plugins()
        )

        # Add whitelisted automatically # TODO
        for f in self.available_plugins:
            self.bot.add_plugin(f())
            LOGGER.info('PLUGIN LOADED: ' + f.__name__)

        # main control buckle
        LOGGER.info('Connected !')
        try:
            print("?>", end='')
            cmd = input('')
            while not self.finished:
                self.finished = not self.bot.is_connected()
                self.do_command(cmd)
                if not self.finished: 
                    print("?>", end='')
                    cmd = input('')
        except KeyboardInterrupt:
            self.bot.disconnect()
        except EOFError:
            self.bot.disconnect()

        LOGGER.info('Disconnected !')
        # finalize all treatments
        self.bot_thread.join()


# PUBLIC METHODS ##############################################################
    def do_command(self, msg):
        """Operate given message as command"""
        LOGGER.info('CMD:' + str(msg))
        for rgx, cmd in self.commands.items():
            if rgx.match(msg):
                LOGGER.info('Internal command:' + str(cmd))
                cmd(rgx.findall(msg))


# PRIVATE METHODS #############################################################
    def __bot_add_sudoer(self, regex_result):
        """add asked sudoer to bot sudoers list"""
        LOGGER.debug(regex_result)
        LOGGER.debug('not implemented !')
        #self.bot.add_sudoer(regex_result[0][0])


    def __bot_disconnect(self, regex_result):
        """disconnect and quit all"""
        self.bot.disconnect()
        self.finished = True


    def __bot_speak(self, regex_result):
        """print message in canal"""
        self.bot.send_message(regex_result[0])
        LOGGER.debug('Said:' + str(regex_result[0]))


    def __plugins(self, regex_result):
        """management of plugins"""
        command = regex_result[0][1].split(' ')
        command, values = command[0], command[1:]
        error_code = {
            'name'  : 'need a valid plugin name',
            'id'    : 'need a valid plugin index',
        }
        error = None

        # listing
        if command in ('list', 'l', 'ls'):
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
        if command in ('print', 'p', 'pr'):
            for fn in (str(f) for f in self.bot.plugins):
                print(str(fn))
        # activation
        elif command in ('activate', 'a', 'ac'):
            if len(values) > 1:
                for name in values:
                    clss = config.import_plugin(name)
                    for cls in clss:
                        self.bot.add_plugin(cls())
            else:
                error = 'name'
        # deactivation
        elif command in ('deactivate', 'd', 'dc'):
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


    def __last_words(self, regex_result):
        """Show last words of IRC"""
        raise NotImplemented


# PREDICATS ###################################################################
# ACCESSORS ###################################################################
# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



