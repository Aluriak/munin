mnn:
	python3 -m munin

tt:
	pylint munin/__main__.py

irc:
	watch tail -n 20 logs/munin.log

ir:
	tail -n 100 logs/munin.log
