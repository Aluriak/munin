# -*- coding: utf-8 -*-
#########################
#      PLUGINS          #
#########################


#########################
# IMPORTS               #
#########################
import re




#########################
# PRE-DECLARATIONS      #
#########################



#########################
# PLUGIN BASE CLASS     #
#########################
class Plugin():
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


# CONSTRUCTOR #################################################################
    def __init__(self):
        self.id = Plugin.NEXT_ID
        Plugin.NEXT_ID += 1


# PUBLIC METHODS ##############################################################
    def accept_message(self, message, sudo=False, author=None):
        """message is the complete message received from IRC
        This method return None if Plugin don't need to 
         react to the message.
        Else, returned value will be received by do_command method.
        """
        return self.regex().fullmatch(message)

    def do_command(self, bot, message, matched_groups=None, sudo=False, author=None):
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


# CONVERSION ##################################################################
    def __str__(self):
        return str(self.id) + ': ' + self.__class__.__name__


# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



