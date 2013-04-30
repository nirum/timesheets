#!/usr/local/bin/python3
"""
tman v0.1.0
simple time management scripts
(c) 2013 benjamin.naecker@gmail.com
"""

## core python imports
import json, os

## tman imports
from help import *
from core import *
#from search import *

## some pretty printing constants
bold = '\033[1m'
under = '\033[4m'
norm = '\033[0m'

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
		if matchProjectName(prefs, projectName):
			print('project {b}{p}{n} already exists'.format(b=bold, p=projectName, n=norm))

		else:
			# if not, create a new project!
			print('creating new project {b}{p}{n}'.format(b=bold, p=projectName, n=norm))
			project = createNewProject(prefs, projectName)
			saveProject(prefs, projectName, project)

	# exit
	os.sys.exit()

## check in on the requested project
if cmd == 'in':
	# check that project name is given
	if nArgs == 1:
		# no project was given
		printUsage('in')
	else:
		# project given, check that it exists
		inputName = args[1]

		# match projectName to input
		projectName = matchProjectName(prefs, inputName)

		if projectName is not None:
			# load the project
			project = loadProject(prefs, projectName)

			# parse the remaining argument list
			rtime, rtag, notes, notice = parseOptArgs(args[2:], project, projectName, prefs)

			# get the currently active project, if any
			currentProject = activeProject(prefs)
			
			# clock in, if not already on another project, or if specific tag requested
			if currentProject is None or rtag is not None:

				# get the current time in the preferred format
				otime = makeTimestamp(prefs)

				# update project timestamp
				t = adjustTime(otime, rtime, prefs)

				# check that a user-requested tag belongs to the requested project
				if rtag is not None and rtag not in project.keys():
					print('requested tag {b}{tg}{n} is not valid for project {b}{p}{n}'.format(b=bold, 
						tg=rtag, n=norm, p=projectName))
					os.sys.exit()

				# make correct tag
				tag = makeEventTag(t, rtag, prefs, clockout=False)

				# clock in!
				print('clocking in on project {b}{p}{n} at {a}{f}'.format(b=bold, p=projectName, n=norm, a=notice, f=t))
				clockIn(prefs, projectName, project, t, tag, notes)

				# save project
				saveProject(prefs, projectName, project)
			else:
				print('you are already clocked in on project {b}{p}{n}'.format(b=bold, p=currentProject[0], n=norm))
				os.sys.exit()
		else:
			print('project {b}{p}{n} does not exist'.format(b=bold, p=inputName, n=norm))
			os.sys.exit()

## check out on the requested project
if cmd == 'out':
	# check that project name is given
	if nArgs == 1:
		# no project was given
		printUsage('out')
	else:
		# project given, check that it exists
		inputName = args[1]

		# match projectName to input
		projectName = matchProjectName(prefs, inputName)

		if projectName is not None:

			# load the project
			project = loadProject(prefs, projectName)

			# parse the remaining argument list
			rtime, rtag, notes, notice = parseOptArgs(args[2:], project, projectName, prefs)

			# check that the project is active now
			currentProject = activeProject(prefs)

			# clock out, if current project exists and is the one requested, or if specific tag requested
			if (currentProject is not None and currentProject[0] == projectName) or rtag is not None:

				# get the current time in the preferred format
				otime = makeTimestamp(prefs)

				# update project timestamp
				t = adjustTime(otime, rtime, prefs)

				# check that a user-requested tag belongs to the requested project
				if rtag is not None and rtag not in project.keys():
					print('requested tag {b}{tg}{n} is not valid for project {b}{p}{n}'.format(b=bold, 
						tg=rtag, n=norm, p=projectName))
					os.sys.exit()

				# make correct tag
				tag = makeEventTag(t, rtag, prefs, clockout=True)

				# clock out!
				print('clocking out on project {b}{p}{n} at {a}{f}'.format(b=bold, p=projectName, n=norm, a=notice, f=t))
				clockOut(prefs, projectName, project, t, tag, notes)

				# save project
				saveProject(prefs, projectName, project)

			else:
				print('you are not currently clocked in on project {b}{p}{n}'.format(b=bold, p=projectName, n=norm))
				os.sys.exit()
		else:
			print('project {b}{p}{n} does not exist'.format(b=bold, p=inputName, n=norm))
			os.sys.exit()

## remove the requested project
if cmd == 'rm':
	# check project name is given
	if nArgs == 1:
		# no project given
		printUsage('rm')
		os.sys.exit()
	else:
		# project name given
		# first check for force argument
		if '-f' in args:
			force = True
			inputName = args[2]
			idx = 3
		else:
			force = False
			inputName = args[1]
			idx = 2

		# match project name to input
		projectName = matchProjectName(prefs, inputName)

		if projectName is not None:

			# load project
			project = loadProject(prefs, projectName)

			# parse the remaining argument list
			rtime, rtag, notes, notice = parseOptArgs(args[idx:], project, projectName, prefs)

			# check if we're deleting a project or a tag
			if rtag is None:
				# deleting entire project!
				# verify that user really wants to delete the project
				if not force:
					really = input('really delete project {b}{p}{n}? all data will be lost. (y/[n]): '.format(b=bold, p=projectName, n=norm))
					if really.lower() not in ['y', 'yes']:
						print('project {b}{p}{n} not removed'.format(b=bold, p=projectName, n=norm))
						os.sys.exit()

				# user really wants to delete, load project
				project = loadProject(prefs, projectName)

				# remove actual data file
				try:
					os.remove(os.path.join(os.path.expanduser(prefs['tmandir']), 'projects', projectName + '.json'))
				except:
					print('could not remove project {b}{p}{n}'.format(b=bold, p=projectName, n=norm))
					os.sys.exit()

				# remove project from metadata file
				md = readMetadata(prefs)
				md['projects'].remove(projectName)
				if md['active'] is not None and len(md['active']) > 1 and md['active'][0] == projectName:
					md['active'] = None

				# write metadata back
				writeMetadata(prefs, md)

				# notify
				print('project {b}{p}{n} removed'.format(b=bold, p=projectName, n=norm))
				os.sys.exit()

			else:
				# deleting tag
				# verify user really wants to delete the tag
				if not force:
					really = input('really delete tag {b}{t}{n} for project {b}{p}{n}? all data will be lost. (y/[n]): '.format(
						b=bold, p=projectName, n=norm, t=rtag))
					if really.lower() not in ['y', 'yes']:
						print('tag {b}{t}{n} for project {b}{p}{n} not removed'.format(b=bold, p=projectName, n=norm, t=rtag))
						os.sys.exit()

				# user really wants to delete tag, load project
				project = loadProject(prefs, projectName)

				# remove selected tag
				removed = project.pop(rtag)

				# save project file
				saveProject(prefs, projectName, project)

				# remove this tag from metadata, if it's the active tag
				md = readMetadata(prefs)
				if md['active'] is not None and md['active'][1] == rtag:
					md['active'] = None

				# write metadata back
				writeMetadata(prefs, md)

				# notify and exit
				print('tag {b}{t}{n} for project {b}{p}{n} removed'.format(b=bold, p=projectName, n=norm, t=rtag))
				os.sys.exit()

		else:
			print('project {b}{p}{n} does not exist'.format(b=bold, p=inputName, n=norm))
			os.sys.exit()

## show information about the current project
if cmd == 'show':
	# check that a project name is given
	if nArgs == 1:
		printUsage('show')
		os.sys.exit()
	else:
		inputName = args[1]
	
	# match input name to project name
	projectName = matchProjectName(prefs, inputName)

	if projectName is not None:
		# load project
		project = loadProject(prefs, projectName)

		# pretty print project
		prettyPrintProject(project, projectName, width=30)
		os.sys.exit()

	else:
		print('project {b}{p}{n} does not exist'.format(b=bold, p=inputName, n=norm))
		os.sys.exit()

## list all projects
if cmd == 'list':
	prs = os.listdir(os.path.join(os.path.expanduser(prefs['tmandir']), 'projects'))
	if len(prs) == 0:
		print('you have no projects!')
	else:
		# get metadata
		md = readMetadata(prefs)
		if md['active'] is not None:
			activeProject = md['active'][0]
		print('your projects are:')
		for p in prs:
			pr = p.replace('.json', '')
			if pr == activeProject:
				print(pr + ' < ')
			else:
				print(pr)
			
