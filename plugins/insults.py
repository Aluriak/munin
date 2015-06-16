#!/usr/bin/python3
# -*- coding: utf-8 -*-

# imports
from munin.functionnalities import Functionnality
from random import randint, choice
import re

# Class 	: Insulte
# Resume	: Get some love from a bot you poor little boy/girl
class Insulte(Functionnality):
	"""
	Insult someone with style
	example:
		Plopp	| bot: insult Nedgang
		bot		| Plopp chie sur le visage de Nedgang
	"""

#	REGEX	= re.compile(r"\s*insult\s+((.+\s+)+)")		# aluriak 2nd try
	REGEX	= re.compile(r"\s*insult((\s+.+)+)")		# plopp 1st try

	# Constructor
	def __init__(self):
		super().__init__()

	def do_command(self, bot, matched_groups, sudo=False, author=None):
		love = ''
		line = ''

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
			if user == '': continue
			if user in open('../data/whitelist.txt').read():
				love += user + " est le ciel, " + user + " est la terre..\n" + user + " est l\'alpha et l\'omega !\n"
			elif randint(0,1) == 0:
				line = choice(open('../data/data.txt').readlines()).strip()
				love += user + ' ' + choice(liste_prefixe_exclam) + 'que ' + line + '!\n'
			else:
				line = choice(open('../data/data.txt').readlines()).strip()
				love += user + ' ' +  choice(liste_prefixe_interrog) + 'que ' + line + '?\n '


		return love


	@property
	def help(self):
			return "INSULTE: get some love from munin."
