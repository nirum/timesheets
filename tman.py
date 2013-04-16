#!/usr/local/bin/python3
"""
simple time management scripts
"""

## VERSION INFO
verString = '''
tman v0.0.1
simple time management scripts
(c) 2013 benjamin.naecker@gmail.com
'''

## core python imports
import argparse, json, sys
from dateutil.parser import time

## tman imports
from help import *
from core import *

## read tman.conf file
try:
	#tmanConfFid = open('~/.tman/tman.conf', 'r')
	tmanConfFid = open('/Users/bnaecker/FileCabinet/Code/tman/tman.conf', 'r')
	tman = json.load(tmanConfFid)
except:
	print('tman not setup, run "python3 setup.py install"')
	sys.exit()

## get primary command input
# get the command, if any
if len(sys.argv) == 1:
	cmd = None
else:
	cmd = sys.argv[1]

# print version string
if cmd == '-v' or cmd == '--version':
	print(verString)
	sys.exit()

# print help if no command given, or -h, --help given
if cmd is None or cmd == '-h' or cmd == '--help' or cmd == 'help':
	# get possible command for which user needs help
	if len(sys.argv) <= 2:
		helpCmd = 'general'
	else:
		helpCmd = sys.argv[2]
	
	# print the usage and quit
	printUsage(helpCmd)
	sys.exit()

## make new project file
if cmd == 'new':
	# check that project name or tag is given
	if len(sys.argv) == 2:
		# if no project given, print usage for new command and exit
		printUsage('new')
		sys.exit()
	else:
		# project given, check that it exists
		projectName = sys.argv[2]
		checkProjectExists(projectName)
		print('project "' + projectName + '" already exists')
		sys.exit()

