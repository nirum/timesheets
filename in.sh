#!/bin/bash
#
# in.sh
#
# start the work timer
#
# (c) bnaecker@stanford.edu 08 Apr 2013

# get current date
dt=$(date +"%d%b%y")

# check that the file exists
filename=~/FileCabinet/Code/innout/timesheets/$dt.txt
if [ -f $filename ]
then
	echo "clocking in at $(date +"%H:%M")"
else
	echo "no timesheet!" 
	~/FileCabinet/Code/innout/newday.sh
	echo "clocking in at $(date +"%H:%M")"
fi

# start the timer
echo -n $(date +"%s") >> $filename
