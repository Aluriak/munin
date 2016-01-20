# -*- coding: utf-8 -*-
#########################
#      PLUGINS          #
#########################
"""
Definition of the base class Plugin.

Plugins system allow Munin IRC Bot to be fully extendable.
"""

#########################
# IMPORTS               #
#########################
import re


PRINTINGS_PLUGINS_MAX_WIDTH = 20


class Plugin:
    """
    Body of a Plugin implementation.
    Inherit from this class is not useless, but not necessary:
    some treatments can be facilitate. (notabily automatic import)

    It just show what is necessary with docstring.
    Best examples are already created plugins.
    """
    # default REGEX that is used for determined if
    # plugin must be called, and with whitch parameters.
    REGEX   = re.compile(r"(.*)")
    NEXT_ID = 1
    SAVE_FILE_PREFIX  = 'data/'
    SAVE_FILE_SUFFIX  = '.plugin'


    def __init__(self, bot):
        self.id = Plugin.NEXT_ID
        Plugin.NEXT_ID += 1
        self.bot = bot


    def accept_message(self, message, sudo=False):
        """message is the complete message received from IRC
        This method return None if Plugin don't need to
         react to the message.
        Else, returned value will be received by do_command method.
        """
        return self.regex().fullmatch(message.message)

    def do_command(self, bot, message, matched_groups=None, sudo=False):
        """Execute command for bot, according to regex matchs, sudo mode

        Return a string that will be sended by the bot. Not that string
        will be cut in multiple messages in place of \n character.
        """
        raise NotImplementedError

    def say_something(self):
        """Say something. Called only when self.want_speak() returned True.

        If a specialization don't have to tell something without order of anothers
        IRC users, this method don't need an overriding."""
        raise NotImplementedError


    def filename(self, basename, prefix=SAVE_FILE_PREFIX,
                 suffix=SAVE_FILE_SUFFIX):
        """Return the filename of a file with given basename.
        Prefix and suffix are by default given by Plugin class"""
        return prefix + basename + suffix

    def want_speak(self):
        """Return True iff self have something to say

        If a specialization don't have to tell something without order of anothers
        IRC users, this method don't need an overriding."""
        return False


    @classmethod
    def regex(cls):
        """Return regex used for match and receive things about message

        Specializations don't have to override this methodes if they defines their
        own REGEX class constant."""
        return cls.REGEX

    @property
    def help(self):
        """Return short documentation about plugin and its command, usability, interests,…"""
        raise NotImplementedError

    @property
    def only_on_explicit_dest(self):
        """True if message must be processed only if the bot is the recipient"""
        return True


    def __str__(self):
        return (str(self.id) + ': ' + self.__class__.__name__).ljust(PRINTINGS_PLUGINS_MAX_WIDTH)
