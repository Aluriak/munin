"""
The IRC Bot itself.

Derived of IRCBot class of irclib,
it provide lots of tools and automatize many behaviors.

Can be controlled by Control instances.
"""

import irc.bot
import irc.strings
import irc.client
import re
import time
import threading

from munin import config
from munin import ircmessage

try:
    from munin.configuration import SERVER, PORT, CHANNEL, NICKNAME, REALNAME
    from munin.configuration import PASSWORD, CHECK_TIME, SUDOERS
except ImportError:
    print(
        'No config file found !\n',
        'Please create your own like munin/configuration_template.py',
        'named munin/configuration.py.'
    )
    exit(0)



#########################
# PRE-DECLARATIONS      #
#########################
LOGGER = munin.config.logger()



#########################
# CLASS                 #
#########################
class Bot(irc.bot.SingleServerIRCBot):
    """
    IRC bot designed for plugin improvements. 

    self.plugins associate a regex to an object that have that API:
        function regex() -> a re compiled regex object
        function do_command(bot, regex_findall) -> 
    """


# CONSTRUCTOR #################################################################
    def __init__(self, nickname=NICKNAME, realname=REALNAME, 
                 server=SERVER, port=PORT, channel=CHANNEL, 
                 check_time=CHECK_TIME, sudoers=SUDOERS):
        super().__init__([(server, port)], nickname, realname)
        self.plugins    = set()  # activated plugins
        self.channel    = channel
        self.nickname   = nickname
        self.sudoers    = sudoers
        self.check_time = check_time

        # check Plugins, if some have something to say
        def wait(): time.sleep(self.check_time)
        def check_timer(bot_instance):
            wait()
            while bot_instance.is_connected():
                bot_instance.check_plugins()
                wait()
        self.check_func_thread = threading.Thread(target=check_timer, args=[self])
        self.check_func_thread.start()


    def send_message(self, msg, dest=None, private=False):
        """"""
        if private is True: assert(private is True and dest is not None)
        assert(msg is not None)
        assert(msg is not '')
        try:
            if private is True:
                self.connection.privmsg(dest, msg)
            else:
                if dest in (None, ' ', ''):
                    self.connection.privmsg(self.channel, msg)
                else:
                    self.connection.privmsg(self.channel, dest + ': ' + msg)
        except irc.client.MessageTooLong:
            LOGGER.warning('ERROR: too long message')
            self.connection.privmsg(self.channel, 'too long message')
        return None

    def add_plugin(self, func):
        """Get instance of plugin, and add it to the list of observers"""
        self.plugins.add(func)

    def rmv_plugin(self, func):
        """remove given plugin
        Return False iff KeyError.
        """
        removed = True
        try:
            self.plugins.remove(func)
        except KeyError:
            removed = False
        return removed

    def rmv_index(self, index):
        """remove plugins with given index
        Return False iff no plugin removed.
        """
        before = len(self.plugins)
        self.plugins = {
            f
            for f in self.plugins
            if f.id != index
        }
        return len(self.plugins) != before

    def check_plugins(self):
        """Check plugins, and give them a chance to speak"""
        for func in self.plugins:
            if func.want_speak():
                self.send_message(func.say_something())

    def add_sudoer(self, name):
        """add given name to sudoers"""
        self.__sudoers.add(name)

    def do_command(self, message, author=None):
        """send message to plugins"""
        for fnc in self.plugins:
            # shortcuts
            sudo = author in self.__sudoers
            accepted = fnc.accept_message(message, sudo, author)
            # if plugin accept the message, call it and send messages
            if accepted is not None:
                responses = (_ for _ in 
                             fnc.do_command(self, message,
                                            accepted.groups(),
                                            sudo, author
                                           ).split('\n')
                             if len(_) > 0
                )
                [self.send_message(r) for r in responses]

    def disconnect(self):
        """Disconnect from IRC, and finish"""
        LOGGER.info('disconnected from IRC')
        try:
            self.connection.quit('Good Bye !')
        except irc.client.ServerNotConnectedError:
            pass
        self.check_func_thread.join()
        self.die()


    def on_nicknameinuse(self, c, e):
        """If nickname already used, add _ at the end and go on"""
        self.nickname = self.nickname + '_'
        LOGGER.warning('nickname used, switch to ' + self.nickname)
        c.nick(self.nickname)

    def on_welcome(self, c, e):
        """When connected to server, join targeted channel"""
        c.join(self.channel)
        self.connection = c
        LOGGER.info('connect to ' + self.channel)

    def on_privmsg(self, c, e):
        assert(c == self.connection)
        author = e.source.nick
        message = e.arguments[0]
        LOGGER.info(author + ' published: ' + message)

    def on_pubmsg(self, c, e):
        """Call plugin if message is a command message"""
        assert(c == self.connection)
        author = e.source.nick
        all_message = e.arguments[0]

        # get target of msg and msg itself
        if all_message.startswith(self.nickname + ':'):
            dest, message = all_message.split(':', 1)
            assert(dest+':'+message == all_message)
        else:
            dest, message = None, all_message
        LOGGER.info(author + ': ' + message + ((' for '+dest) if dest is not None else ''))

        # lookup plugins for received command 
        if dest == self.nickname:
            self.do_command(message, author)



    def is_connected(self):
        return self.connection.is_connected()

    def __contains__(self, o):
        """Return True iff o is a Plugin subclass that have
        an instance in currently runned plugins.
        """
        return any(o is p.__class__ for p in self.plugins)
