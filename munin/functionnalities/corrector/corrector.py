# -*- coding: utf-8 -*-
#########################
#       DICE            #
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
class Corrector(Functionnality):
    """
    Simple Functionnality application.
    Repeat last sentence of user that correct it by using a regex.
    example:
        lucas| hellp
        lucas| s/p/o
        bot  | lucas would say: hello
    """
    REGEX     = re.compile(r"(.*)")
    REGEX_RGX = re.compile(r"s/([^/]+)\/([^/]+)/?.*")


# CONSTRUCTOR #################################################################
    def __init__(self):
        super().__init__()
        self.last_words = {} # author:last message


# PUBLIC METHODS ##############################################################
    def do_command(self, bot, matched_groups, sudo=False, author=None):
        """Execute command for bot (unused), 
        according to regex matchs (used) and sudo mode (unused)"""
        results = ''
        # if its a correction
        regres = Corrector.REGEX_RGX.fullmatch(matched_groups[0])
        if regres is not None:
            # author need a correction 
            regres = regres.groups()
            if author in self.last_words:
                try:
                    regex   = re.compile(regres[0])
                    replace = regres[1] if len(regres) > 1 else ''
                    self.last_words[author] = re.sub(regex, 
                                                     replace, 
                                                     self.last_words[author]
                                                    )
                    results = self.last_words[author]
                    results += ' «««« corrected ' + author + ' words'
                except:
                    results = author + ' would say something i don\'t recognize'
        else:
            # get last message of author
            self.last_words[author] = matched_groups[0]
        return results



# PRIVATE METHODS #############################################################
# PREDICATS ###################################################################
# ACCESSORS ###################################################################
    @property
    def help(self):
        return """CORRECTOR: apply regex as s/// format to your last sentence. Useless but fun."""


# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



