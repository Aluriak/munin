# -*- coding: utf-8 -*-
#########################
#       HELPER          #
#########################


#########################
# IMPORTS               #
#########################
from munin.functionnalities import Functionnality
import re




#########################
# PRE-DECLARATIONS      #
#########################



#########################
# CLASS                 #
#########################
class Helper(Functionnality):
    """
    Simple Functionnality application.
    Provide some help on current bot functionnalities.
    """
    REGEX = re.compile(r"\s*help([0-9 ]+)*\s*")


# CONSTRUCTOR #################################################################
    def __init__(self):
        super().__init__()


# PUBLIC METHODS ##############################################################
    def do_command(self, bot, matched_groups, sudo=False, author=None):
        """Execute command for bot (used), 
        according to regex matchs (used) and sudo mode (unused)"""
        if matched_groups[0] is None:
            # general help
            results = (
                'This bot can be found as source code here: '+
                'http://github.com/aluriak/munin\n' 
                + ' ; '.join((str(i) + ':' + f.__class__.__name__ 
                              for i, f in enumerate(bot.functionnalities))
                            )
            )
        else: 
            # matched_groups have a number that correspond maybe to a functionnality
            indexes = {int(_) for _ in matched_groups[0].split(' ') if _ is not ''}
            results = '\n'.join((f.help for i, f in enumerate(bot.functionnalities) if i in indexes))
        return results


# PRIVATE METHODS #############################################################
# PREDICATS ###################################################################
# ACCESSORS ###################################################################
    @property
    def help(self):
        return "HELPER: wait for 'help [n]' command, for general help or about bot or its functionnalities."
# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



