#CHAN=--channel=\#test_munin

CONFIG_FILE=config.json
OPTIONS=$(CHAN)


mnn:
	python3 -m munin $(CONFIG_FILE) $(OPTIONS)

tt:
	pylint munin/__main__.py

irc:
	watch tail -n 20 logs/munin.log

ir:
	tail -n 100 logs/munin.log
