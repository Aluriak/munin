# -*- coding: utf-8 -*-
#########################
#       HELPER          #
#########################


#########################
# IMPORTS               #
#########################
from munin.plugin import Plugin
import re




#########################
# PRE-DECLARATIONS      #
#########################



#########################
# CLASS                 #
#########################
class Helper(Plugin):
    """
    Simple Plugin application.
    Provide some help on current bot plugins.
    """
    REGEX = re.compile(r".*help([0-9 ]+)*\s*")


# CONSTRUCTOR #################################################################
    def __init__(self, bot):
        super().__init__(bot)


# PUBLIC METHODS ##############################################################
    def do_command(self, bot, message, matched_groups=None, sudo=False):
        """Execute command for bot (used),
        according to regex matchs (used) and sudo mode (unused)"""
        if matched_groups[0] is None:
            # general help
            results = (
                'This bot can be found as source code here: '+
                'http://github.com/aluriak/munin\n'
                + ' ; '.join((str(i) + ':' + f.__class__.__name__
                              for i, f in enumerate(bot.plugins))
                            )
            )
        else:
            # matched_groups have a number that correspond maybe to a plugin
            indexes = {int(_) for _ in matched_groups[0].split(' ') if _ is not ''}
            results = '\n'.join((f.help for i, f in enumerate(bot.plugins) if i in indexes))
        return results


    @property
    def help(self):
        return "HELPER: wait for 'help [n]' command, for general help or about bot or its plugins."
