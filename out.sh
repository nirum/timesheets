#!/bin/bash
#
# out.sh
#
# stop the work timer
#
# (c) bnaecker@stanford.edu 08 Apr 2013

# get the date
dt=$(date +"%d%b%y")

# check the file exists
filename=~/FileCabinet/Code/innout/timesheets/$dt.txt
if [ -f $filename ]
then
	echo "clocking out at $(date +"%H:%M")"

	# stop the clock
	echo -e $(date +"\t%s") >> $filename
else
	echo "no timesheet, no timer"
fi
