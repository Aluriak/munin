mkdir -p $1
echo "from $1 import *" > $1/__init__.py
cd $1
/home/lucas/Programmation/Perl/makesrc/makesrc.pl py -n $1
cd ..
