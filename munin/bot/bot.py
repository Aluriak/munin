"""
The IRC Bot itself.

Derived of IRCBot class of irclib,
it provide lots of tools and automatize many behaviors.

Can be controlled by Control instances.
"""

import re
import time
import random
import threading

import irc.bot
import irc.strings
import irc.client

from munin import config
from munin import ircmessage

try:
    from munin.configuration import SERVER, PORT, CHANNEL, NICKNAME, REALNAME
    from munin.configuration import PASSWORD, CHECK_TIME, SUDOERS, EXPRESSIVITY, EXPRESSIONS
except ImportError:
    print(
        'No config file found !\n',
        'Please create your own like munin/configuration_template.py',
        'named munin/configuration.py.'
    )
    exit(0)


LOGGER = config.logger()


class Bot(irc.bot.SingleServerIRCBot):
    """IRC bot designed for allowing plugin improvements"""


    def __init__(self, nickname=NICKNAME, realname=REALNAME,
                 server=SERVER, port=PORT, channel=CHANNEL,
                 check_time=CHECK_TIME, sudoers=SUDOERS,
                 expressions=EXPRESSIONS, expressivity=EXPRESSIVITY):
        super().__init__([(server, port)], nickname, realname)
        self.plugins      = set()  # activated plugins
        self.channel      = channel
        self.nickname     = nickname
        self.sudoers      = sudoers
        self.check_time   = check_time
        self.expressions  = tuple(expressions)
        self.expressivity = float(expressivity)
        assert 0. <= self.expressivity <= 1.

        # check Plugins, if some have something to say
        def wait(): time.sleep(self.check_time)
        def check_timer(bot_instance):
            wait()
            while bot_instance.is_connected():
                bot_instance.check_plugins()
                wait()
        self.check_func_thread = threading.Thread(target=check_timer, args=[self])
        self.check_func_thread.start()


    def send_message(self, msg, dest=None, private=False, expressionable=True):
        """"""
        if private is True: assert(private is True and dest is not None)
        assert(msg is not None)
        assert(msg is not '')
        if random.random() < self.expressivity and not any(msg.endswith(c) for c in ':!?…'):
            msg = msg.rstrip('.  …') + ', ' + self.expression
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
        """Get instance of plugin, and add it to the list of plugins"""
        self.plugins.add(func)

    def has_plugin(self, func):
        """True if given plugin is used"""
        return func in self.plugins

    def del_plugin(self, *, func=None, idx=None):
        """remove given plugin, by reference xor id in the plugin dict.
        Return True iff a plugin was removed.
        """
        assert bool(func) != bool(idx)  # one, and only one
        if idx:
            filtered_plugins = {p for p in self.plugins if p.id != idx}
            removed = len(filtered_plugins) < len(self.plugins)
            self.plugins = filtered_plugins
            assert len(filtered_plugins) <= len(self.plugins)
        if func:
            try:
                self.plugins.remove(func)
            except KeyError:
                removed = False
        return removed

    def check_plugins(self):
        """Check plugins, and give them a chance to speak"""
        for func in self.plugins:
            if func.want_speak():
                self.send_message(func.say_something())

    def add_sudoer(self, name):
        """add given name to sudoers"""
        self.sudoers.add(name)

    def do_command(self, message):
        """send message to plugins"""
        for plugin in self.plugins:
            if plugin.only_on_explicit_dest and message.dest != self.nickname:
                continue  # the plugin is not interested by this message
            # shortcuts
            sudo = message.author in self.sudoers
            accepted = plugin.accept_message(message, sudo)
            # if plugin accept the message, call it and send messages
            if accepted is not None:
                responses = (r for r in plugin.do_command(self, message,
                                                          accepted.groups(),
                                                          sudo).split('\n')
                             if len(r) > 0
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
        message = ircmessage.IRCMessage(e.arguments[0], e.source.nick)
        LOGGER.info(author + ' published: ' + str(message))

    def on_pubmsg(self, c, e):
        """Call plugin if message is a command message"""
        assert(c == self.connection)
        message = ircmessage.IRCMessage(e.arguments[0], e.source.nick)
        LOGGER.info(message)
        self.do_command(message)


    def is_connected(self):
        return self.connection.is_connected()

    def __contains__(self, o):
        """Return True iff o is a Plugin subclass that have
        an instance in currently runned plugins.
        """
        return any(o is p.__class__ for p in self.plugins)

    @property
    def expression(self):
        try:
            return random.choice(self.expressions)
        except IndexError:
            return ''
