"""
Definition of the base class Plugin.

Plugins system allow Munin IRC Bot to be fully extendable.

"""

import pickle
import re


PRINTINGS_PLUGINS_MAX_WIDTH = 20


class Plugin:
    """
    Body of a Plugin implementation.
    Inherit from this class is heavily encouraged, as many treatments on plugins
    (especially the data persistence) are already implemented.

    Some functions are useful to redefine:
        - do_command, defining the behavior of the module
        - only_on_explicit_dest, defining if all messages must be treated
        - debug_data, defining things to print when user want to get an overview of internal data
        - help, defining the string returned on IRC when help is asked
        - persistent_data, defining data to be stored
        - persistent_filename, defining the filename where data is saved

    Best examples of redefinition usage are the already created plugins.

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

    @property
    def debug_data(self):
        return self.__class__.__name__

    @property
    def persistent_data(self):
        """Return the data that must be saved, or None if no persistence needed"""
        return None

    @persistent_data.setter
    def persistent_data(self, values):
        pass  # nothing to do

    @property
    def persistent_filename(self):
        """Basename (without extension) of the file used
        to store data of the plugin

        default is the lowered class name

        """
        return self.__class__.__name__.lower()

    def filename(self, basename, prefix=SAVE_FILE_PREFIX,
                 suffix=SAVE_FILE_SUFFIX):
        """Return the filename of a file with given basename.
        Prefix and suffix are by default given by Plugin class"""
        return prefix + basename + suffix

    def save_persistent_data(self):
        """Get data in filename, save it in the filename"""
        payload = self.persistent_data
        if payload is not None:
            with open(self.filename(self.persistent_filename), 'wb') as fd:
                pickle.dump(payload, fd)

    def load_persistent_data(self):
        """Load data in the filename, or use the default_persistant_data()"""
        try:
            with open(self.filename(self.persistent_filename), 'rb') as fd:
                self.persistent_data = pickle.load(fd)
        except (IOError, EOFError):
            self.persistent_data = self.default_persistant_data()

    def default_persistant_data(self):
        """Return the default persistent data"""
        return None

    def __str__(self):
        return (str(self.id) + ': ' + self.__class__.__name__).ljust(PRINTINGS_PLUGINS_MAX_WIDTH)
