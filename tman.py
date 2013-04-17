#!/usr/local/bin/python3
"""
tman v0.0.1
simple time management scripts
(c) 2013 benjamin.naecker@gmail.com
"""

## core python imports
import argparse, json, os
from dateutil.parser import time

## tman imports
from help import *
from core import *

## read tman.conf file
try:
	fid = open(os.path.expanduser('~/.tman/tman.conf'))
	prefs = getTmanPrefs(fid)
except:
	print('tman not setup, you gotta do some stuff first')
	os.sys.exit()

## get the input arguments
nArgs = len(os.sys.argv) - 1
if nArgs == 0:
	args = None
else:
	args = os.sys.argv[1:]

## get primary command input
# get the command, if any
if nArgs == 0:
	cmd = None
else:
	cmd = args[0]

# print version string
if cmd == '-v' or cmd == '--version':
	print(__doc__)
	os.sys.exit()

# print help if no command given, or -h, --help given
if cmd is None or cmd == '-h' or cmd == '--help' or cmd == 'help':
	# get possible command for which user needs help
	if nArgs < 2:
		# print general help if user doesn't specify a command
		helpCmd = 'general'
	else:
		# print help for a specific command
		helpCmd = args[1]
	
	# print the usage and quit
	printUsage(helpCmd)
	os.sys.exit()

## make new project file
if cmd == 'new':
	# check that project name or tag is given
	if nArgs == 1:
		# if no project given, print usage for new command and exit
		printUsage('new')
		os.sys.exit()
	else:
		# project given, check that it exists
		projectName = args[1]
		projectExists = checkProjectExists(makeProjectFilename(prefs, projectName))
		if projectExists:
			print('project "' + projectName + '" already exists')
			os.sys.exit()

		# if not, creat a new project!
		project = createNewProject(prefs, projectName)
		saveProject(project)

