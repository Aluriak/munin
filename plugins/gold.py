"""
Gold point management.

"""
from collections import defaultdict, deque
import random
import pickle
import re

from munin.plugin import Plugin


class Gold:
    """
    Unit of gold, registering the donator, the receiver, and the message
    that motivate the donation.
    Moreover, the gold initially pushed.
    """
    INITIAL_GOLD_COUNT = 20

    def __init__(self, donator, receiver, message, old_gold):
        self.donator, self.receiver, self.message = donator, receiver, message
        self.old = old_gold


class GoldManager(Plugin):
    """
    Gold point management :
        - each nick have an initial amount of point
        - each nick can give a gold to any other
        - with each transaction is saved the last words of the receivers
    """
    REGEX    = re.compile(r"\s*(.*)")
    REGEX_GG = r"g(?:ive)?\s?g(?:old)?\s+([^\s]+)\s*(.*)?"
    REGEX_MG = r"m(?:y)?\s?g(?:old)?\s*"
    REGEX_GO = r"g(?:old)?\s?o(?:f)?\s+([^\s]+)\s*"
    REGEX_GM = r"g(?:ive)m(?:egold)\s+(.+)\s*"
    REGEX_RS = r"reset gold"

    GOLD_FILE = 'gold'

    def __init__(self, bot):
        super().__init__(bot)
        self.last_words = {'munin': "I'm a stegausorus !"} # author: last message
        self.gold = self.default_persistant_data()
        # regexes management
        prefix = self.bot.nickname + ':?\s*'
        self.reg_givegold   = re.compile(prefix + GoldManager.REGEX_GG)
        self.reg_givealias  = re.compile(         GoldManager.REGEX_GG)
        self.reg_givemegold = re.compile(prefix + GoldManager.REGEX_GM)
        self.reg_mygold     = re.compile(prefix + GoldManager.REGEX_MG)
        self.reg_goldof     = re.compile(prefix + GoldManager.REGEX_GO)
        self.reg_resetgold  = re.compile(prefix + GoldManager.REGEX_RS)


    def do_command(self, bot, message, matched_groups=None, sudo=False):
        """Execute command for bot (unused),
        according to regex matchs (used) and sudo mode (unused)"""
        results = ''
        author = message.author
        # if its a correction
        reg_gm = self.reg_givemegold.fullmatch(message.all)
        reg_rg = self.reg_resetgold.fullmatch(message.all)
        reg_ga = self.reg_givealias.fullmatch(message.all)
        reg_gg = self.reg_givegold.fullmatch(message.all)
        reg_ag = self.reg_mygold.fullmatch(message.all)
        reg_go = self.reg_goldof.fullmatch(message.all)
        if reg_gg or reg_ga:
            reg_gg = reg_gg if reg_gg else reg_ga
            receiver = reg_gg.groups()[0]
            reason = reg_gg.groups()[1] if reg_gg.groups()[1] else self.last_words.get(receiver, None)
            if receiver is None:
                results += 'but ' + receiver + ' have never say anything !'
            elif len(self.gold[author]) > 0:
                self.give_gold(receiver, donator=author, reason=reason)
                results += author + " send gold to " + receiver + ' for '
                if reason:
                    results += '«' + reason + '»\n'
                else:
                    results += 'no reason\n'
            else:
                results += author + " don't have enough gold !\n"
        elif reg_gm:  # someone want to get gold
            reason = reg_gm.groups()[0]
            if self.accept(reason, author) and self.give_gold(author, reason=reason):
                results += "You're so cute, " + self.bot.expression
                results += " ; please get your gold :)"
            else:
                results += "So much imagination you have !"
        elif reg_ag:  # author want to know its gold amount
            if author in self.gold:
                results += author + ': you have ' + str(len(self.gold[author])) + ' gold. '
                results += self.random_gold_owner_comparison(author) + '\n'
            else:
                results += author + ': you have no gold, sorry.'
        elif reg_go:  # author wants to know how many gold have someone
            receiver = reg_go.groups()[0]
            if receiver in self.gold:
                results += receiver + ' has ' + str(len(self.gold[receiver])) + ' gold.'
            else:
                results += "I don't know " + receiver
        elif reg_rg and author in self.bot.sudoers:  # author wants to reset golds
            self.reset_gold()
            results += ('All golds have been removed. New golds are available '
                        'through ' + self.bot.nickname)
        else:  # author don't write a regex ; whatever it is, it's now its last words
            self.last_words[author] = matched_groups[0]
        return results

    @property
    def help(self):
        return """GOLD: give gold to another people with the givegold command."""

    @property
    def only_on_explicit_dest(self):
        return False  # react on all messages

    def random_gold_owner(self):
        try:
            return random.choice(tuple(self.gold))
        except IndexError:
            return None

    def random_gold_owner_comparison(self, name):
        other = self.random_gold_owner()
        mygold = len(self.gold[name])
        if name != other and other is not None:
            other_gold = len(self.gold[other])
            if mygold > other_gold:
                term = 'more than'
            elif mygold < other_gold:
                term = 'less than'
            else:
                term = 'as much as'
            return 'Thus, you have ' + term + ' ' + other + '...\n'
        return ''

    def give_gold(self, receiver, donator=None, reason='administration'):
        if donator is None:
            donator = self.bot.nickname
        try:
            oldgold = self.gold[donator].popleft()
            self.gold[receiver].append(Gold(
                donator, receiver, reason, oldgold
            ))
        except IndexError:
            return False
        return True

    def accept(self, reason, author):
        """Return True if given reason is sufficient for get a gold"""
        return author in self.bot.sudoers

    def reset_gold(self):
        """Reset all golds. Note : all gold are loss"""
        self.gold = defaultdict(deque) # author: deque(gold instances)
        self.gold[self.bot.nickname] = deque(
            Gold(self.bot.nickname, self.bot.nickname, 'initial gold', None)
            for _ in range(Gold.INITIAL_GOLD_COUNT)
        )

    @property
    def initial_gold_count(self):
        return self.gold[self.bot.nickname]

    @initial_gold_count.setter
    def initial_gold_count(self, value):
        self.gold[self.bot.nickname] = int(value)
        assert value >= 0

    @property
    def persistent_data(self):
        return self.gold

    @persistent_data.setter
    def persistent_data(self, values):
        self.gold = values

    @property
    def debug_data(self):
        return self.gold

    def default_persistant_data(self):
        """Return the default persistent data"""
        golds = deque(
            Gold(None, self.bot.nickname, str(i), None)
            for i in range(Gold.INITIAL_GOLD_COUNT)
        )
        return {self.bot.nickname: golds}  # dict {nickname: golds}
