"""
Messager plugin for Munin.

"""
from collections import defaultdict
from munin.plugin import Plugin
from random import randint
import re


class Hermes(Plugin):
    """
    Messager application, where anyone can leave a message to anyone.

    """
    REGEX    = re.compile(r"\s*(.*)\s*")
    REGEX_LM = re.compile(r"\s*msgto\s*([^\s,;]+)\s*(.+)\s*")
    REGEX_GM = re.compile(r"\s*mymsg\s*")


    def __init__(self, bot):
        super().__init__(bot)
        self.messages = self.default_persistant_data()


    def do_command(self, bot, message, matched_groups=None, sudo=False):
        """Execute command for bot (unused), according to regex matchs (used) and sudo mode (unused)"""
        results = ''
        author = message.author
        dest = message.dest
        leave_message = Hermes.REGEX_LM.fullmatch(message.message)
        get_message = Hermes.REGEX_GM.fullmatch(message.message)
        # print('DEBUG:', leave_message, get_message)

        if dest == self.bot.nickname:
            if leave_message:
                receiver, leaved_msg = leave_message.groups()
                print('LEAVED MSG:', author, 'to', receiver, ':', leaved_msg)
                self.messages[receiver][author] = leaved_msg
            if get_message:
                # print('GET MSG:', self.messages)
                if author in self.messages:
                    for sender, msg in self.messages[author].items():
                        results += 'From ' + sender + ': ' + msg + '\n'
                    del self.messages[author]
        return results

    @property
    def help(self):
        return ("""HERMES: leave a message with 'bot: msgto gérard mymessage', """
                """and get yours with 'bot: mymsg'""")

    @property
    def debug_data(self):
        return self.messages

    @property
    def persistent_data(self):
        return self.messages

    @persistent_data.setter
    def persistent_data(self, values):
        self.messages = values

    def default_persistant_data(self):
        """Return the default persistent data"""
        return defaultdict(dict)  #  {receiver:{author: message}}
