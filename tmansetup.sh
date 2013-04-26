#!/bin/bash
#
# tmansetup.sh is a setup script for the tman time management system.
# It will ask for a location to store tman-related files and ask if 
# you'd like to add tman to /usr/local/bin or make it an alias in your
# bashrc.
#
# (c) 2013 benjamin.naecker@gmail.com

## print a welcome
BOLD=`tput bold`
NORMAL=`tput sgr0`
echo -e "Welcome to ${BOLD}tman${NORMAL}, a simple time managment system\n"

## ask for location
echo -e "Where would you like to put tman files?"
read -p "This includes source code and project JSON files. [~/.tman]: " TMANDIR
if [ -z $TMANDIR ]; then
	TMANDIR=~/.tman
fi
if [ -d $TMANDIR ]; then
	echo "Sorry, $TMANDIR already exists!"
	echo "Exiting setup"
	exit 0
fi
echo "Copying files to $TMANDIR"
mkdir -p $TMANDIR
mkdir $TMANDIR/projects

## copy stuff!
cp ./*.py $TMANDIR/
cp ./*.md $TMANDIR/
cp -R ./.git* $TMANDIR/
# copy this script itself...so meta
cp ./tmansetup.sh $TMANDIR/

## ask for timestamp format
echo -e "\nHow would you like timestamps displayed?"
read -p "This can be any of the standard representations recognized by 'strftime'. [%c]: " TIMEFMT
if [ -z $TIMEFMT ]; then
	TIMEFMT='%c'
fi

## actually make tmanrc
echo -e "[Core]" >> $HOME/.tmanrc
echo -e "tmandir = $TMANDIR" >> $HOME/.tmanrc
echo -e "timefmt = $TIMEFMT" >> $HOME/.tmanrc

## put something in /usr/local/bin?
echo ""
read -p "Would you link to symlink tman to /usr/local/bin? [y]/n: " DOLINK
if [ -z $DOLINK ]; then
	DOLINK='y'
fi
if [ $DOLINK = 'y' ]; then
	echo -e "Please enter your sudo password to symlink tman"
	sudo ln -sf $TMANDIR/tman.py /usr/local/bin/tman
	chmod u+x /usr/local/bin/tman
else
	echo -e "Adding an alias to tman for this session only."
	echo -e "Please add an alias to your shell initilization files."
	alias tman=$TMANDIR/tman.py
fi


## that's all for now
echo -e "\nThat's it, you're all setup to use tman."
echo -e "Type 'tman --help' or 'tman help <command>' to learn more about how to use tman."
