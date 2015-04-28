#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
# imports
from munin.functionnalities import Functionnality
from random import randint, choice
import re
 
# Class         : Insulte
# Resume        : Get some love from a bot you poor little boy/girl
class Insult(Functionnality):
        """
        Insult someone with style
        example:
                Plopp   | bot: insult Nedgang
                bot             | Plopp chie sur le visage de Nedgang
        """
 
        REGEX   = re.compile(r"\s*insulte((\s+.+)+)")
 
        # Constructor
        def __init__(self):
                super().__init__()
 
        def do_command(self, bot, matched_groups, sudo=False, author=None):
                love = ''
                users_count = 0
 
                # Liste des suffixes d'interpellation interrogatives
                liste_prefixe_interrog = [
                        "Tu savais ",
                        "On t'as déjà dit ",
                        "T'avais remarqué ",
                        "Tu te rendais compte "
                ]
 
                # Liste des préfixes d'interpellation exclamatives
                liste_prefixe_exclam = [
                        "Tout le monde sait ",
                        "Il est démontré ",
                        "Tu devrais te rappeler ",
                        "Oublis pas "
                ]
 
 
                for u in matched_groups[0].split(' '):
                        user = u.lower()
                        if ' ' == str(user): continue
                        if user in ['neolem', 'plopp', 'aluriak']:
                                love += user + " est bon et ne peut être insulté tellement sa perfection est parfaite. C\'est un être aussi proche du divin que celui qui à voulu l\'insulter est proche de la merde. \nIl est le ciel et la terre.\nIl est l\'alpha et l\'omega.\n\n"
                        elif user == 'nedgang':
                                love += user + " t\'es Charmant tu sait ? ahahaha.\n\n"
                        elif randint(0,1) == 0:
                                line = choice(open('data/data.txt').readlines())
                                love += user + ' ' + choice(liste_prefixe_exclam) + 'que ' + line + '!\n\n '
                        else:
                                line = choice(open('data/data.txt').readlines())
                                love += user + ' ' +  choice(liste_prefixe_interrog) + 'que ' + line + '?\n\n '
                       
 
                return love
 
 
        @property
        def help(self):
                        return "INSULTE: get some love from munin."
