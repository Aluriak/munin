# -*- coding: utf-8 -*-
#########################
#       DICE            #
#########################


#########################
# IMPORTS               #
#########################
from munin.plugin import Plugin
import re


class Corrector(Plugin):
    """
    Simple Plugin application.
    Repeat last sentence of user that correct it by using a regex.
    example:
        lucas| hellp
        lucas| s/p/o
        bot  | lucas would say: hello
    """
    REGEX     = re.compile(r"(.*)")
    REGEX_RGX = re.compile(r"s/([^/]+)\/([^/]+)/?.*")

    def __init__(self, bot):
        super().__init__(bot)
        self.last_words = {} # author: last message

    def do_command(self, bot, message, matched_groups=None, sudo=False):
        """Execute command for bot (unused),
        according to regex matchs (used) and sudo mode (unused)"""
        results = ''
        author = message.author
        # if its a correction
        regres = Corrector.REGEX_RGX.fullmatch(matched_groups[0])
        if regres is not None:
            # author need a correction
            regres = regres.groups()
            if author in self.last_words:
                try:
                    regex   = re.compile(regres[0])
                    replace = regres[1] if len(regres) > 1 else ''
                    corrected = re.sub(regex, replace, self.last_words[author])
                    if corrected != self.last_words[author]:
                        results = corrected
                        results += ' \t«««« corrected ' + author + ' words'
                        self.last_words[author] = corrected
                except re.sre_constants.error:  # TODO: attribute error
                    # something go wrong with user's regex
                    results += "from the dark side, you're REGEX comes.\n"
        else:  # author don't write a regex ; whatever it is, it's now its last words
            self.last_words[author] = message.all
        return results

    @property
    def help(self):
        return """CORRECTOR: apply regex as s/// format to your last sentence. Useless but fun."""

    @property
    def only_on_explicit_dest(self):
        return False  # react on all messages
