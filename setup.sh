#!/bin/bash
#
# setup.sh
#
# sets up your filesystem for the time management shell scripts
#
# (c) bnaecker@stanford.edu 09 Apr 2013

# banner
echo "tman"
echo "simple time management shell scripts."
echo "(c) benjamin.naecker@gmail.com 2013."
echo "running setup script"
echo ""

# prompt for base directory
#echo -n "where would you like your timesheets to live [~/.innout]: "
read -p "where would you like your timesheets to live? [~/.tman]: " tmandir

# check if it's empty
if [ -z "$tmandir" ]
then
	tmandir='~/.tman'
fi

# make the directory
mkdir $tmandir

# prompt for updating shell aliases
read -p "would you like to update your bashrc with command aliases? [n]: " update

# make a conf file
touch $tmadir/tman.conf
echo "tmandir=$tmandir"

