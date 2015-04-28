# -*- coding: utf-8 -*-
#########################
#       CONTROL            
#########################


#########################
# IMPORTS               #
#########################
import threading
import re

import munin.config



#########################
# PRE-DECLARATIONS      #
#########################
LOGGER          = munin.config.logger()
RGX_SUDOERS_ADD = re.compile(r"\s*sudoers\s+add\s*([a-zA-Z0-9_]*)\s*")
RGX_DISCONNECT  = re.compile(r"\s*(quit|:q)\s*")
RGX_SPEAK       = re.compile(r"\s*say\s(.*)")



#########################
# CLASS                 #
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
            RGX_SUDOERS_ADD: self.__bot_add_sudoer,
            RGX_DISCONNECT : self.__bot_disconnect,
            RGX_SPEAK      : self.__bot_speak,
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

# PREDICATS ###################################################################
# ACCESSORS ###################################################################
# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



