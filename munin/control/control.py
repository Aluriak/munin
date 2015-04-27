# -*- coding: utf-8 -*-
#########################
#       CONTROL            
#########################


#########################
# IMPORTS               #
#########################
import threading
import re
import munin.functionnalities as fnct
#from munin.functionnalities import Admin




#########################
# PRE-DECLARATIONS      #
#########################
RGX_SUDOERS_ADD = re.compile(r" *sudoers add *([a-zA-Z0-9_]*) *")
RGX_DISCONNECT  = re.compile(r" *(quit|:q) *")
RGX_SPEAK       = re.compile(r" *say (.*)")



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

        # Initial functionnalities
        self.available_functionnalities = [f for f in (getattr(fnct, a) for a in fnct.__dir__())
                                           if callable(f) and issubclass(f, fnct.Functionnality) 
                                           # and f.__class__ is not fnct.Functionnality
                                           # and 'functionnality' not in f.__class__.__name__.lower()
                                           and 'functionnality' not in f.__name__.lower()
                                           # and f.__class__.__name__ != fnct.Functionnality.__name__
                                           # and 'functionnality' not in super(f).__class__.__name__.lower()
                                          ]
        for f in self.available_functionnalities:
            print(f.__name__, f.__class__, super(f))
            self.bot.add_functionnality(f())

        # main control buckle
        print('Connected !')
        cmd = input('')
        while not self.finished:
            self.finished = self.bot.is_connected()
            self.do_command(cmd)
            if not self.finished: 
                cmd = input('')

        # finalize all treatments
        self.bot_thread.join()


# PUBLIC METHODS ##############################################################
    def do_command(self, msg):
        """Operate given message as command"""
        print('CMD:', msg)
        for rgx, cmd in self.commands.items():
            if rgx.match(msg):
                print('Understood !', cmd)
                cmd(rgx.findall(msg))


# PRIVATE METHODS #############################################################
    def __bot_add_sudoer(self, regex_result):
        """add asked sudoer to bot sudoers list"""
        print(regex_result)
        print('not implemented !')
        #self.bot.add_sudoer(regex_result[0][0])


    def __bot_disconnect(self, regex_result):
        """disconnect and quit all"""
        self.bot.disconnect()
        self.finished = True


    def __bot_speak(self, regex_result):
        """print message in canal"""
        self.bot.send_message(regex_result[0])
        print('Said:', regex_result[0])

# PREDICATS ###################################################################
# ACCESSORS ###################################################################
# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



