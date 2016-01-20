# -*- coding: utf-8 -*-
#########################
#       DICE            #
#########################


#########################
# IMPORTS               #
#########################
from munin.plugin import Plugin
from random import randint
import re


MAX_DICE_SIZE   = 100
MAX_DICE_NUMBER = 100
MAX_SET_NUMBER  = 10


class DiceLauncher(Plugin):
    """
    Simple Plugin application.
    Wait for something like:
        3d8 1d9 2d20
    each set of dices are launched, and results are returned:
        3d8: {2, 1, 7} 10
        1d9: {3} 3
        2d20: {12, 17} 29
        total: 42
    """
    REGEX = re.compile(r"\s*((?:\s*\d+[dD]\d+)+)")


# CONSTRUCTOR #################################################################
    def __init__(self, bot):
        super().__init__(bot)


# PUBLIC METHODS ##############################################################
    def do_command(self, bot, message, matched_groups=None, sudo=False):
        """Execute command for bot (unused), according to regex matchs (used) and sudo mode (unused)"""
        results = ''
        total   = 0
        dice_set_count = 0

        for dice_set in matched_groups[0].split(' '):
            n, s = dice_set.lower().split('d')
            if '0' in (n, s): continue
            numbers  = [randint(1, int(s)) for _ in range(int(n))]
            total   += sum(numbers)
            results += ('{' 
                        + ', '.join((str(_) for _ in numbers)) 
                        + '} \ttotal: ' + str(sum(numbers)) 
                        + '\n'
                       )
            dice_set_count += 1

        return results + ('total: ' + str(total) if dice_set_count > 1 else '')



# PRIVATE METHODS #############################################################
# PREDICATS ###################################################################
# ACCESSORS ###################################################################
    @property
    def help(self):
        return """DICELAUNCHER: launch dices. Try something like '3d5 3d20', you will understand."""


# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



