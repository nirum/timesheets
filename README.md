Timesheets
==========

Benjamin Naecker
----------------

This is a set of simple shell scripts to log your work hours.
You'll need to update the scripts to work with your filesystem however you
see fit.

newday.sh
---------

This script makes a new text file for the current work day, and starts the 
clock for the first time.

in.sh
-----

This starts the timer.

out.sh
------

This stops the timer

endday.sh
--------

At the end of the workday, this stops the timer for the final time, and
then computes the total hours you worked that day. This is saved in a text
file.

TODO
====

+ update in and out scripts to put in an optional string with whatever you're
working on.
