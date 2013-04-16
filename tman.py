#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3
#
# tman.py
# 
# simple time management
#
# (c) 2013 benjamin.naecker@gmail.com

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


## test first command input

# get command input
if len(sys.argv) == 1:
	cmd = None
else:
	cmd = sys.argv[1]

# print version string
if cmd == '-v' or cmd == '--version':
	print(verString)
	sys.exit()

# print help
if cmd is None or cmd == '-h' or cmd == '--help':
	printGeneralHelp()
	sys.exit()

## make new project file
if cmd == 'new':
	# check that project name or tag is given
	if len(sys.argv) == 2:
		printNewUsage()
		sys.exit()
	
	# look for project/tag requested
	projectTag = sys.argv[2]
	print(projectTag)
