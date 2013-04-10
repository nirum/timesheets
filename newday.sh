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
touch ~/Dropbox/logs/timesheets/$dt.txt

# start the timer
in.sh
