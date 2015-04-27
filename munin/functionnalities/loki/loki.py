# -*- coding: utf-8 -*-
########
# DICE #
########


###########
# IMPORTS #
###########
from munin.functionnalities import Functionnality
import re


####################
# PRE-DECLARATIONS #
####################


#########
# CLASS #
#########
class Loki(Functionnality):
    """
    Simple Functionnality application.
    Repeat last sentence of an user, turnin it pervert.
    example:
        My scars hurts! -> My balls hurts!
    """
    REGEX     = re.compile(r"(.*)")                     # Vas matcher tout les messages -> déclenche corrector à chaque fois
    REGEX_RGX = re.compile(r"munin: loki (.+)")   # Déclencheur (.+) est retourné dans matched_group[0] (do cmd (ln48))


###############
# CONSTRUCTOR #
###############
    def __init__(self):
        super().__init__()
        self.last_words = {} # author:last message


##################
# PUBLIC METHODS #
##################
    def do_command(self, bot, matched_groups, sudo=False, author=None):
        """TO DO"""
        results = ''
        target=matched_groups[0]
        # if its a correction
        regres = Corrector.REGEX_RGX.fullmatch(matched_groups[0])
        if regres is not None:
            # author need a pervert version
            regres = regres.groups()
            if target in self.last_words:
                normal_sentence = self.last_words[target]
                result = _turn_pervert(norm)
        else:
            # get last message of author
            self.last_words[author] = target
        return results


###################
# PRIVATE METHODS #
###################
    def _turn_pervert(base):


# PREDICATS #

#############
# ACCESSORS #
#############
    @property
    def help(self):
        return """TO DO"""


# CONVERSION #
# OPERATORS #




#############
# FUNCTIONS #
#############

