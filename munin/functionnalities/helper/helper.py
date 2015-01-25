# -*- coding: utf-8 -*-
#########################
#       HELPER          #
#########################


#########################
# IMPORTS               #
#########################
import re




#########################
# PRE-DECLARATIONS      #
#########################



#########################
# CLASS                 #
#########################
class Helper():
    """
    Simple Functionnality application.
    Provide some help on current bot functionnalities.
    """
    REGEX = re.compile(r"\s*help\s*(\d+)?.*")


# CONSTRUCTOR #################################################################
    def __init__(self):
        self._regex = self.REGEX


# PUBLIC METHODS ##############################################################
    def do_command(self, bot, matched_groups, sudo=False, author=None):
        """Execute command for bot (used), according to regex matchs (used) and sudo mode (unused)"""
        if matched_groups[0] is None:
            # general help
            results = 'This bot can be found as source code here: http://github.com/aluriak/irc-bot\n' + \
                    ' ; '.join([str(i) + ':' + f.__class__.__name__ for i, f in enumerate(bot.functionnalities)])
        else: 
            # matched_groups have a number that correspond maybe to a functionnality
            print('DEBUX:', matched_groups[0])
            indexes = [int(_) for _ in matched_groups[0].split(' ') if _ is not '']
            results = '\n'.join([f.help for i, f in enumerate(bot.functionnalities) if i in indexes])
        return results


# PRIVATE METHODS #############################################################
# PREDICATS ###################################################################
    def want_speak(self):
        """Return True iff self have something to say"""
        return False


# ACCESSORS ###################################################################
    @property
    def regex(self):
        return self._regex

    @property
    def help(self):
        return "HELPER: wait for 'help [n]' command, for general help or about bot or its functionnalities."
# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



