# -*- coding: utf-8 -*-
#########################
#       BOT             #
#########################


#########################
# IMPORTS               #
#########################
import irc.bot
import irc.strings
try:
    from munin.configuration import SERVER, PORT, CHANNEL, NICKNAME, REALNAME, PASSWORD
except:
    print('No config file found !\nPlease create your own like munin/configuration_template.py named munin/configuration.py.')
    exit(0)
import re
import time
import threading
#from functionnality import GithubWatcher



#########################
# PRE-DECLARATIONS      #
#########################



#########################
# CLASS                 #
#########################
class Bot(irc.bot.SingleServerIRCBot):
    """
    IRC bot designed for functionnality improvements. 

    self.functionnalities associate a regex to an object that have that API:
        function regex() -> a re compiled regex object
        function do_command(bot, regex_findall) -> 
    """
    CHECK_TIME = 5 # time between two functionnalities check


# CONSTRUCTOR #################################################################
    def __init__(self, nickname=NICKNAME, realname=REALNAME, server=SERVER, port=PORT, channel=CHANNEL):
        super().__init__([(server, port)], nickname, realname)
        self.functionnalities = set()
        self.channel   = channel
        self.nickname  = nickname
        self.__sudoers = {'aluriak', 'DrIDK'}

        # check Functionnalities, if some have something to say
        def check_timer(bot_instance):
            time.sleep(Bot.CHECK_TIME)
            while bot_instance.is_connected():
                bot_instance.check_functionnalities()
                time.sleep(Bot.CHECK_TIME)
        self.check_func_thread = threading.Thread(target=check_timer, args=[self])
        self.check_func_thread.start()


# PUBLIC METHODS ##############################################################
    def send_message(self, msg, dest=None, private=False):
        """"""
        if private is True: assert(private is True and dest is not None)
        assert(msg is not None)
        if private is True:
            self.connection.privmsg(dest, msg)
        else:
            if dest in (None, ''):
                self.connection.privmsg(self.channel, msg)
            else:
                self.connection.privmsg(self.channel, dest + ': ' + msg)
        return None

    def add_functionnality(self, func):
        """Get instance of functionnality, and add it to the list of observers"""
        self.functionnalities.add(func)

    def check_functionnalities(self):
        """Check functionnalities, and give them a chance to speak"""
        for func in self.functionnalities:
            if func.want_speak():
                self.send_message(func.say_something())

    def add_sudoer(self, name):
        """add given name to sudoers"""
        self.__sudoers.add(name)

    def log(self, log_msg):
        """logging"""
        print('LOG: ' + log_msg)

    def do_command(self, command, author=None):
        """send command to functionnalities"""
        for fnc in self.functionnalities:
            if fnc.regex is not None:
                matching = re.fullmatch(fnc.regex, command)
                if matching is not None:
                    responses = fnc.do_command(self, matching.groups(), sudo=author in self.__sudoers, author=author)
                    for response in responses.split('\n'):
                        self.send_message(response)


    def disconnect(self):
        """Disconnect from IRC, and finish"""
        print('I\'M KILLED !!')
        self.connection.quit('Good Bye !')
        self.check_func_thread.join()
        self.die()


# IRC METHODS    ##############################################################
    def on_nicknameinuse(self, c, e):
        """If nickname already used, add _ at the end and go on"""
        self.nickname = self.nickname + '_'
        self.log('nickname used, switch to ' + self.nickname)
        c.nick(self.nickname)

    def on_welcome(self, c, e):
        """When connected to server, join targeted channel"""
        c.join(self.channel)
        self.connection = c
        self.log('connect to ' + self.channel)

    def on_privmsg(self, c, e):
        assert(c == self.connection)
        author = e.source.nick
        message = e.arguments[0]
        self.log(author + ' published: ' + message)

    def on_pubmsg(self, c, e):
        """Call functionnality if message is a command message"""
        assert(c == self.connection)
        author = e.source.nick
        all_message = e.arguments[0]

        # get target of msg and msg itself
        if re.fullmatch(re.compile('^' + self.nickname + ": .*") , all_message):
            dest, message = all_message.split(':', 1)
            assert(dest+':'+message == all_message)
        else:
            dest, message = None, all_message
        self.log(author + ' published: ' + message + ((' for '+dest) if dest is not None else ''))

        # launch command (as sudo if necessary)
        #print(dest, message)
        #print('matched !', '[SUDO]' if author in self.__sudoers else '') 
        self.do_command(message, author)
        




# PRIVATE METHODS #############################################################
# PREDICATS ###################################################################
    def is_connected(self):
        return self.connection.is_connected()


# ACCESSORS ###################################################################
# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



