#!/bin/bash
# newday.sh
#
# make new timesheet for the current day
#
# (c) bnaecker@stanford.edu 08 Apr 2013

# get the date
dt=$(date +"%d%b%y")

# notify
echo "making timesheet for $(date +"%d %b %Y")" 

# make the file
touch ~/FileCabinet/Code/innout/timesheets/$dt.txt

# start the timer
~/FileCabinet/Code/innout/in.sh
