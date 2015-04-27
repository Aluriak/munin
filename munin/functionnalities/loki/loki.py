# -*- coding: utf-8 -*-
########
# DICE #
########


###########
# IMPORTS #
###########
from munin.functionnalities import Functionnality
import re
import random


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
                result = _turn_pervert(self.last_words[target])
        else:
            # get last message of author
            self.last_words[author] = target
        return results


###################
# PRIVATE METHODS #
###################
    def _turn_pervert(base):
        key=("ma",  "mes",  "mon")
        reco = tuple((j, j.index()) for j in base.split(" ") if j in key)
        if reco != ():
            return _change(base,  reco[-1])
        else:
            return "Je suis désolé, mais là pour le coup, je ne trouve rien à\
        dire, donc du coup je vais raconter une blague!\n"+_blague()

    def _change(phrase, mot):
        borne=phrase.find(mot)
        if mot == "ma":
            return phrase[0:borne]+"bite "+phrase[borne+3:]
        elif mot == "mes":
            return phrase[0:borne]+"baballes "+phrase[borne+4:]
        elif mot == "mon":
            return phrase[0:borne]+"cul "+phrase[borne+4:]


    def _blague():
        f = open("blagues.txt", 'r')
        lignes = f.readlines()
        f.close()
        compilation = []
        for l in lignes:
            compilation.append(l)
        return compilation[random.randint(0, len(compilation)-1)]

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

