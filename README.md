tman
==========

Benjamin Naecker
----------------

tman is a simple shell script to help you keep track of your work hours.

Usage
-----
tman <command> [options]

Commands
--------

setup		- simple setup. creates tman directory and adds an alias to your bashrc
new			- make a timesheet for today
in [notes]	- start the timer, possibly with notes
out [notes] - stop the timer, possibly with notes
end			- stop the timer for the day, summarize your work hours

TODO
====

+ [x] update in and out scripts to put in an optional string with whatever you're
working on.
+ [x] write using printf to format the timesheet and summary files
+ [ ] check that summary does not already exist before trying to add it to the summary file
+ [ ] move scripts to tman dir at the end of setup
+ [ ] more options? deal with forgetting to logout/summarize, add notes after the fact, etc.
+ [ ] backup? what happens if i delete/overwrite the summary file? maybe have daily backups?
