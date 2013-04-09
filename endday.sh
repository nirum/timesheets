#!/bin/bash
#
# endday.sh
#
# add up the timers for the day
#
# (c) bnaecker@stanford.edu 08 Apr 2013

# get the date
dt=$(date +"%d%b%y")

# some file names
datefile=~/FileCabinet/Code/innout/timesheets/$dt.txt
difffile=~/FileCabinet/Code/innout/timesheets/$dt.tmpdiff
sumfile=~/FileCabinet/Code/innout/hours/$dt.txt

# do the computation
# first check that the file exists
if [ -f $datefile ]
then
	# clock out
	~/FileCabinet/Code/innout/out.sh

	# notify
	echo -n "closing timesheet for $(date +"%d %b %Y") "

	# print the differences to a temp file
	awk '{print ($2 - $1)}' $datefile >> $difffile

	# sum the differences
	awk '{s+=$1} END {print (s / 3600)}' $difffile > $sumfile

	# echo hours worked to the command line
	echo "($(cat $sumfile) hrs)"

	# remove the diff file
	rm $difffile
else
	# do nothing if there is no file
	echo "no timesheet, no timer"
fi
