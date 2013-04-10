#!/bin/bash
#
# tman.sh
#
# tman is a shell script that provides a simple way to log your work day.
# 
# INPUT:
# 	setup					- sets up tman.conf and the directory structure
# 	new						- create new timesheet for today
#	in [notes] 				- clock in, or start the timer, possibly with notes
# 	out [notes]				- clock out, or stop the timer, possibly with notes
# 	end [notes] 			- end the work day, logging the hours worked
# 	show [ summary | date ] - show either the summary file or the timesheet for 
# 							  the requested date
#
# OUTPUT:
# 	tman works with exclusively with text files, which are within the 
# 	directory tmandir, defined in tman.conf
#
# (c) benjamin.naecker@gmail.com 2013
#
# version history:
#	0.0.1	- 	09 Apr 2013
#	0.1.0	- 	10 Apr 2013
# 	0.1.1 	- 	10 Apr 2013

VERSTRING="tman version 0.1.1\n(c) benjamin.naecker@gmail.com 2013"

## input parsing
## --help or no input
if ( [ $# == 0 ] || [ $1 = "--help" ] || [ $1 = "-h" ] )
then
	# print usage
	echo -e $VERSTRING
	echo ""
	echo "usage: tman <command> [options]"
	echo ""
	echo "commands:"
	echo -e "  setup\t\t initial setup of tman"
	echo -e "  new  \t\t create new timesheet for today"
	echo -e "  in   \t\t clock in, optional notes attached"
	echo -e "  out  \t\t clock out, optional notes attached"
	echo -e "  end  \t\t end the day, sum up hours worked"
	echo -e "  show \t\t show either the summary or the timesheet for the requeste date"
	exit 1
fi

## version
if ( [ $1 = "--version" ] || [ $1 = '-v' ] )
then
	# print version
	echo -e $VERSTRING
fi

## commands
case $1 in 
	"setup" ) 
		# check if TMANDIR is a shell variable
		if [ -z "$TMANDIR" ]
		then
			# notify
			echo "setting up tman"

			# prompt for a TMANDIR
			read -p "where would you like tman to reside? [~/.tman]: " TMANBASEDIR

			# make a directory there
			if [ -z "$TMANBASEDIR" ]
			then
				TMANBASEDIR=~
			fi
			TMANDIR="$TMANBASEDIR/.tman"

			# just another safety check
			if [ -d $TMANDIR ]
			then
				echo  "tman is already setup here, exiting"
				exit 1
			fi
			mkdir $TMANDIR

			# make the tman.conf file
			TMANCONF=$TMANDIR/tman.conf
			touch $TMANCONF

			# export the TMANDIR
			echo "export TMANDIR=$TMANDIR" >> $TMANCONF
	
			## check if the user wants to make aliases
			read -e -p "would you like to add an alias for tman? [y]: " ADDALIAS
			if [ -z "$ADDALIAS" ]
			then
				# add the alias to the tman.conf file
				echo "alias tman=$TMANDIR/tman.sh" >> $TMANCONF

				# actually do these commands
				alias tman=$TMANDIR/tman.sh
				export TMANDIR=$TMANDIR

				## add them to the bashrc
				# check that a bashrc exists
				if [ -f ~/.bashrc ]
				then
					# if so, source the tman.conf on bash startup
					echo "" >> ~/.bashrc
					echo "# sourcing the tman.conf file" >> ~/.bashrc
					echo "source $TMANCONF" >> ~/.bashrc

				else
					# if not, notify
					echo "WARNING: no bashrc found. tman alias will not work out of the box"
				fi

			fi

			# add the timesheets directory
			mkdir "$TMANDIR/timesheets"

			# notify we're done
			echo "tman is all set up, you're ready to roll"
		
		else
			echo "tman is already set up"
		fi;;
	"new" )
		# get current day
		DAY=$(date +"%d%b%Y")

		# file name for this day's time sheet
		DAYFILE=$TMANDIR/timesheets/$DAY.txt
		
		# check if it exists
		if [ -f $DAYFILE ]
		then
			echo "timesheet for $(date +"%d %b %Y") already exists"
			exit 1
		else
			echo "making timesheet for $(date +"%d %b %Y")"
		fi

		# make the timesheet
		touch $DAYFILE

		# put up the headers
		printf "%-16s" "--- IN ---" >> $DAYFILE
		printf "%-32s" "--- NOTES ---" >> $DAYFILE
		printf "%-16s" "--- OUT ---" >> $DAYFILE
		printf "%-32s\n" "--- NOTES ---" >> $DAYFILE

		# start the timer
		echo "clocking in at $(date +"%H:%M")"
		printf "%-16s" "$(date +"%s")" >> $DAYFILE

		# check if there are any clockin notes
		if [ $# -le 1 ]
		then
			NOTES="none"
		else
			NOTES=$2
		fi

		# cat the notes
		printf "%-32s" "$NOTES" >> $DAYFILE
		;;
	"in" )
		# get current day
		DAY=$(date +"%d%b%Y")

		# file name for this day's time sheet
		DAYFILE=$TMANDIR/timesheets/$DAY.txt
		
		# check if it exists
		if ! [ -f $DAYFILE ]
		then
			echo "timesheet for $(date +"%d %b %Y") does not exist"
			exit 1
		fi

		# start the timer
		echo "clocking in at $(date +"%H:%M")"
		printf "%-16s" "$(date +"%s")" >> $DAYFILE

		# check if there are any clockin notes
		if [ $# -le 1 ]
		then
			NOTES="none"
		else
			NOTES=$2
		fi

		# cat the notes
		printf "%-32s" "$NOTES" >> $DAYFILE
		;;
	"out" )
		# get current day
		DAY=$(date +"%d%b%Y")

		# filename for this day's timesheet
		DAYFILE=$TMANDIR/timesheets/$DAY.txt

		# check if it exists
		if ! [ -f $DAYFILE ]
		then
			echo "timesheet for $(date +"%d %b %Y") does not exist"
			exit 1
		fi

		# stop the timer
		echo "clocking out at $(date +"%H:%M")"
		printf "%-16s" "$(date +"%s")" >> $DAYFILE

		# check if there are any clockout notes
		if [ $# -le 1 ]
		then
			NOTES="none"
		else
			NOTES=$2
		fi

		# cat the notes, this time printing a new line
		printf "%-32s\n" "$NOTES" >> $DAYFILE
		;;
	"end" )
		# get current day
		DAY=$(date +"%d%b%Y")

		# filename for this day's timesheet
		DAYFILE=$TMANDIR/timesheets/$DAY.txt

		# check if it exists
		if ! [ -f $DAYFILE ]
		then
			echo "timesheet for $(date +"%d %b %Y") does not exist"
			exit 1
		fi

		# check if a summary file exists
		SUMFILE=$TMANDIR/summary.txt
		if ! [ -f $SUMFILE ] 
		then
			touch $SUMFILE
			printf "%-16s" "--- DATE ---" >> $SUMFILE
			printf "%-24s\n" "--- HOURS ---" >> $SUMFILE
		fi
		# NEED TO CHECK IF DATE IS ALREADY THERE!
		# put the date in the sumfile
		#echo -en "$(date +"%d %b %Y"):\t" >> $SUMFILE
		printf "%-16s" "$(date +"%d %b %Y"):" >> $SUMFILE

		# stop the timer
		echo "clocking out at $(date +"%H:%M")"
		printf "%-16s" "$(date +"%s")" >> $DAYFILE

		# check if there are any clockout notes
		if [ $# -le 1 ]
		then
			NOTES="none"
		else
			NOTES=$2
		fi

		# cat the notes, this time printing a new line
		printf "%-32s\n" "$NOTES" >> $DAYFILE

		# count up the hours worked and print to the summary file
		TMPFILE=$TMANDIR/timesheets/$DAY.temp
		awk '$1 ~ /[0-9]/ {print ($3 - $1)}' $DAYFILE >> $TMPFILE
		awk '{s+=$1} END {print (s / 3600)}' $TMPFILE >> $SUMFILE
		
		# NEED TO PRINT TODAY'S HOURS TO COMMAND LINE

		# remove temporary diff file
		rm $TMPFILE
		;;
	"show" )
		# get current day
		DAY=$(date +"%d%b%Y")

		# check second argument
		if  ( [ $# -le 1 ] ||  [ $2 = "summary" ] )
		then
			# check the summary file exists
			SUMFILE=$TMANDIR/summary.txt
			if [ -f $SUMFILE ]
			then
				# print out summary file
				echo "summary of your work hours"
				echo ""
				cat $TMANDIR/summary.txt
				echo ""
			else
				echo "summary file does not exist yet."
				echo ""
			fi
		else
			# print out the timesheet for the requested day
			if [ -f $TMANDIR/timesheets/$2.txt ]
			then
				echo "timesheet for $2"
				cat $TMANDIR/timesheets/$2.txt
				echo ""
			else
				echo "timesheet for $2 does not exist"
			fi
		fi
		;;
esac
