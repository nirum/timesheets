#!/usr/local/bin/python3
"""
tman v0.0.2
simple time management scripts
(c) 2013 benjamin.naecker@gmail.com
"""

## core python imports
import json, os, time

## tman imports
from help import *
from core import *

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

## read tmanrc file
rcfile = os.path.expanduser('~/.tmanrc')
if os.path.isfile(rcfile):
	prefs = getTmanPrefs(rcfile)
else:
	printSetupHelp()
	os.sys.exit()

## make new project file
if cmd == 'new':
	# check that project name or tag is given
	if nArgs == 1:
		# if no project given, print usage for new command
		printUsage('new')
	else:
		# project given, check that it exists
		projectName = args[1]
		if checkProjectExists(makeProjectFilename(prefs, projectName)):
			print('project "' + projectName + '" already exists')

		else:
			# if not, create a new project!
			project = createNewProject(prefs, projectName)
			saveProject(project)

	# exit
	os.sys.exit()

## check in on the requested project
if cmd == 'in':
	# check that project name is given
	if nArgs is 1:
		# no project was given
		print(nArgs)
		printUsage('in')
	else:
		# project given, check that it exists
		projectName = args[1]
		if checkProjectExists(makeProjectFilename(prefs, projectName)):
			# load the project
			project = loadProject(prefs, projectName)

			# check that the project is active now
			if not isActive(project):

				# get the current time in the preferred format
				t = makeTimestamp(prefs)

				# check notes is a string
				if nArgs is 3:
					notes = args[2]
				else:
					notes = ''
				if type(notes) is not str:
					printUsage('in')
					os.sys.exit()

				# clock in!
				print('clocking in on project "' + projectName + '" at ' + t)
				clockIn(prefs, project, t, notes)

				# save project
				saveProject(project)
			else:
				print('you are already clocked in on project "' + projectName + '"')
				os.sys.exit()
		else:
			print('project "' + projectName + '" does not exist')
			os.sys.exit()

## check out on the requested project
if cmd == 'out':
	# check that project name is given
	if nArgs is 1:
		# no project was given
		printUsage('out')
	else:
		# project given, check that it exists
		projectName = args[1]
		if checkProjectExists(makeProjectFilename(prefs, projectName)):
			# load the project
			project = loadProject(prefs, projectName)

			# check that the project is active now
			if isActive(project):

				# get the current time in the preferred format
				t = makeTimestamp(prefs)

				# check notes is a string
				if nArgs is 3:
					notes = args[2]
				else:
					notes = ''
				if type(notes) is not str:
					printUsage('out')
					os.sys.exit()

				# clock out!
				print('clocking out on project "' + projectName + '"at ' + t)
				clockOut(prefs, project, t, notes)

				# save project
				saveProject(project)

			else:
				print('you are not currently clocked in on project "' + projectName +'"')
				os.sys.exit()
		else:
			print('project "' + projectName + '" does not exist')
			os.sys.exit()

## list all projects
if cmd == 'list':
	projects = [f.rstrip('.json') for f in os.listdir(os.path.join(os.path.expanduser(prefs['tmandir']), 'projects'))]
	print('your projects are:')
	for pr in projects:
		print(pr)

