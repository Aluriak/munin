# -*- coding: utf-8 -*-
#########################
#   FUNCTIONNALITIES    #
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
class Functionnality():
    """
    Body of a Functionnality implementation.
    Inherit from this class is not useless, but not necessary:
    some treatments can be facilitate. (notabily automatic import)

    It just show what is necessary with docstring.
    Best examples are already created functionnalities.

    Note that __init__.py of Functionnality module is dedicated 
    to functionnality import. Use it for facilitate access to your 
    functionnality from Control class.
    """
    # default REGEX that is used for determined if 
    # functionnality must be called, and with whitch parameters.
    REGEX = re.compile(r"")


# CONSTRUCTOR #################################################################
    def __init__(self):
        pass


# PUBLIC METHODS ##############################################################
    def do_command(self, bot, matched_groups, sudo=False, author=None):
        """Execute command for bot, according to regex matchs, sudo mode, and author
        
        Return a string that will be sended by the bot. Not that string
        will be cut in multiple messages in place of \n character.
        """
        raise NotImplementedError

    def say_something(self):
        """Say something. Called only when self.want_speak() returned True.
        
        If a specialization don't have to tell something without order of anothers
        IRC users, this method don't need an overriding."""
        raise NotImplementedError



# PRIVATE METHODS #############################################################
# PREDICATS ###################################################################
    def want_speak(self):
        """Return True iff self have something to say
        
        If a specialization don't have to tell something without order of anothers
        IRC users, this method don't need an overriding."""
        return False


# ACCESSORS ###################################################################
    @property
    def regex(self):
        """Return regex used for match and receive things about message

        Specializations don't have to override this methodes if they defines their
        own REGEX class constant."""
        return self.REGEX

    @property
    def help(self):
        """Return short documentation about functionnality and its command, usability, interests,…"""
        raise NotImplementedError

# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



