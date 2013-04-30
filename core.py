import os, json, re
from datetime import datetime, timedelta

# printing constants
bold = '\033[1m'
under = '\033[4m'
norm = '\033[0m'

## preferences
def getTmanPrefs(filename):
	"""read tmanrc INI file"""
	# import configparser`
	from configparser import ConfigParser

	# read in the INI file
	cp = ConfigParser()
	cp.read(filename)

    # assign to prefs dictionary
	prefs = {}
	for sec in cp.sections():
		for opt in cp.options(sec):
			prefs[opt] = cp.get(sec, opt, raw=True)

	return prefs

# project creation and removal
def makeProjectFilename(prefs, projectName):
	"""make a full filename for the given project"""
	return os.path.join(os.path.expanduser(prefs['tmandir']), 'projects', projectName + '.json')

def createNewProject(prefs, projectName):
	"""create a new project with the given name"""
	# create an empty project dict
	project = {}
	#project = {'in': [], 
			   #'out': [],
			   #'notes': []}

	# add the project to the metadata file
	addProjectToMd(prefs, projectName)

	return project

def removeProject(prefs, projectName, force=False):
	"""remove a project with the given name"""
	# verify user wants to do this

## timestamp stuff
def makeTimestamp(prefs):
	"""return a string timestamp according to the user's preferred format"""
	# generate an actual timestamp
	timestamp = datetime.now()

	# return the string-formatted timestamp 
	return datetime.strftime(timestamp, prefs['timefmt'])

def getTimestamps(project):
	return project['timestamps']

def adjustTime(t, rtime, prefs):
	"""adjust clockout time to that provided by user"""
	if rtime == '0':
		# no time difference requested, just return original timestamp
		return t

	if rtime[0] in ['-', '+']:
		# user-requested time is relative to current time
		# check for plus/minus, days, hours, and minutes
		diffs = [float(li) for li in re.split('[-+dhm]', rtime) if len(li) > 0]

		# insert zeros where missing indices
		missIdx = [['d', 'h', 'm'].index(si) for si in 
				[di for di in ['d', 'h', 'm'] if di not in rtime]]
		for ii in missIdx:
			diffs.insert(ii, 0.0)

		# make a time delta object with the requested differences
		td = timedelta(days=diffs[0], minutes=diffs[2], hours=diffs[1])

		# add or subtract it
		if rtime[0] is '-':
			return datetime.strftime(datetime.strptime(t, prefs['timefmt'])
					 - td, prefs['timefmt'])
		else:
			return datetime.strftime(datetime.strptime(t, prefs['timefmt'])
					+ td, prefs['timefmt'] )
   # elif re.match('yesterday', rtime) is not None:
		## requested time is -1 day
		#diffs[0] = -1
	#elif re.search('tomorrow', rtime) is not None:
		## requested time is +1 day
		#diffs[0] = 1
	#elif re.search('ago', rtime) is not None:
		## requested time is -n days
		#diffs[0] = -float(rtime[0:
	#elif: re.search('from now', rtime) is not None:

## event tags
def makeEventTag(timestamp, inputTag, prefs, clockout=True):
	"""return a hex tag for the given timestamp"""
	if inputTag is not None:
		# user specified a tag, just return it
		return inputTag
	else:
		# check if we're clocking out
		if clockout:
			md = readMetadata(prefs)
			return md['active'][1]
		else:
			# make random number with timestamp as seed, convert to hex
			import random
			random.seed(timestamp)
			return hex(int(str(random.random()).lstrip('0.'))).lstrip('0x')

## clocking in and out
def clockIn(prefs, projectName, project, t, tag, notes):
	"""clock in on a project"""
	# check if new key, i.e., NOT updating and therefore need to define empty dict
	if tag not in project.keys():
		# brand new tag, initialize empty dictionary
		project[tag] = {}
		project[tag]['out'] = 0
		project[tag]['outnotes'] = ''

	# update the project dictionary with the clock in time and its notes
	project[tag]['in'] = t
	project[tag]['innotes'] = notes
	
	# set the project as active
	setActive(prefs, projectName, tag)

def clockOut(prefs, projectName, project, t, tag, notes):
	"""clock out on a project"""
	# note should never get here without project[tag] already existing, and we'll always overwrite
	project[tag]['out'] = t
	project[tag]['outnotes'] = notes

	# set project as inactive
	setInactive(prefs)

## set/get active project
def activeProject(prefs):
	"""return the currently active project and the tag to the last clock event"""
	# read metadata.json
	md = readMetadata(prefs)

	# check if project is active 
	return md['active']


def setActive(prefs, projectName, tag):
	"""set a project as active"""
	# read current metadata
	md = readMetadata(prefs)

	# list the current project as active, and set the tag
	md['active'] = [projectName, tag]

	# write metadata
	writeMetadata(prefs, md)
	
def setInactive(prefs):
	"""set a project as inactive"""
	# read current metadata
	md = readMetadata(prefs)

	# list None as the active project
	md['active'] = None

	# write metadata
	writeMetadata(prefs, md)
	
## save/load project
def saveProject(prefs, projectName, project):
	"""save a project to its file"""
	# open the file
	fid = open(os.path.join(os.path.expanduser(prefs['tmandir']), 'projects', projectName + '.json'), 'w')
	json.dump(project, fid)
	fid.close()

def loadProject(prefs, projectName):
	"""load the JSON project object with the given name"""
	# assume it exists!
	fid = open(os.path.join(os.path.expanduser(prefs['tmandir']), 'projects', projectName + '.json'), 'r')
	project = json.load(fid)
	fid.close()

	return project

def matchProjectName(prefs, projectName):
	"""match project name to existing projects, if possible"""
	# read metadata JSON file
	md = readMetadata(prefs)

	# direct match case
	if projectName in md['projects']:
		return projectName
	
	# guess which experiment they requested
	mt = [re.match(projectName, pi) for pi in md['projects']]
	if not any(mt):
		# no possible matches
		projectName = None
	else:
		# find matches
		matches = [md['projects'][i] for i, x in enumerate([re.match(projectName, pi) for pi in md['projects']]) if x is not None]
		
		# deal with matches
		if len(matches) == 1:
			# if only one match, just choose it, but notify the user
			print('autocompleting project {b}{pi}{n} to {b}{pf}{n}\n'.format(b=bold, pi=projectName, pf=matches[0], n=norm))
			projectName = matches[0]
		else:
			# more than one match, let user pick
			print('the following projects match the input {b}{p}{n}.\n'.format(b=bold, p=projectName, n=norm))
			for mi in range(len(matches)):
				print('  [{m}] - {s}'.format(m=mi, s=matches[mi]))

			# get selection and validate
			sel = -1
			while sel < 0 or sel >= len(matches):
				sel = int(input('please select one: '))

			# get that project name
			projectName = matches[sel]

	# return the actual projectName
	return projectName
			
## metadata stuff
def readMetadata(prefs):
	"""read the metadata.json file"""
	fid = open(os.path.join(prefs['tmandir'], 'metadata.json'), 'r')
	md = json.load(fid)
	fid.close()
	return md

def writeMetadata(prefs, md):
	"""write the metadata.json file"""
	fid = open(os.path.join(prefs['tmandir'], 'metadata.json'), 'w')
	json.dump(md, fid)
	fid.close()

def addProjectToMd(prefs, projectName):
	"""add the project with the given name to the metadata file"""
	# read current metadata
	md = readMetadata(prefs)
	
	# add this project to the list
	md['projects'].append(projectName)

	# save the new metadata
	writeMetadata(prefs, md)

## parse optional input arguments
def parseOptArgs(optargs, project, projectName, prefs):
	"""parse input arguments"""
	# when no optional input arguments given
	if len(optargs) == 0:
		rtime = '0'
		rtag = None
		notes = ''
		notice = ''	
		return rtime, rtag, notes, notice
	else:
		# some optional arguments specified, parse away!
		# check for each possibility, and remove it from args as it is found
		
		# first check for a tag
		hasTag = [re.match('--tag', ai) for ai in optargs]
		if any(hasTag):
			# user requested specific tag
			# pop the full arg off optargs list
			fullarg = optargs.pop([mi is None for mi in hasTag].index(False))
			
			# get requested tag, potentially a partial match
			rtagpart = re.sub('--tag=', '', fullarg)

			# try to match it to a tag for the given project
			mt = [re.match(rtagpart, ti) for ti in project.keys()]
			if not any(mt):
				# user-requested tag cannot possibly match project...abort abort!
				print('requested tag {b}{t}{n} has no possible matches for project {b}{p}{n}!'.format(b=bold, t=rtagpart, p=projectName, n=norm))
				os.sys.exit()
			else:
				# user-requested tag has some possible matches
				# find matches
				tags = [ti for ti in project.keys()]
				matches = [tags[i] for i, x in enumerate([re.match(rtagpart, ti) for ti in project.keys()]) if x is not None]

				# deal with matches
				if len(matches) == 1:
					# if only one match, just choose it but notify user
					print('autocompleting tag {b}{ti}{n} to {b}{tf}{n}'.format(b=bold, ti=rtagpart, tf=matches[0], n=norm))
					rtag = matches[0]
				else:
					# multiple matches, let user pick
					print('the following tags match the input {b}{t}{n} for project {b}{p}{n}\n'.format(b=bold, t=rtagpart, n=norm, p=projectName))
					for mi in range(len(matches)):
						print('  [{m}] - {s}'.format(m=mi, s=matches[mi]))

					# get selection and validate
					sel = -1
					while sel < 0 or sel >= len(matches):
						sel = int(input('please select one: '))

					# get that tage name
					rtag = matches[sel]

		else:
			# user did not request a specific tag
			# assume that we're clocking out of the currently active project
			md = readMetadata(prefs)
			if md['active'] is not None:
				rtag = md['active'][1]
			else:
				rtag = None

		# check remaining arguments for time
		hasTime = [re.match('--time', ai) for ai in optargs]
		if any(hasTime):
			# user requested specific time
			# pop full arg off optargs list
			fullarg = optargs.pop([mi is None for mi in hasTime].index(False))

			# get requested time
			rtime = re.sub('--time=', '', fullarg)
			notice = 'adjusted time of '
		else:
			# user did not request specific time
			rtime = '0'
			notice = ''

		# check if any remaining arguments, which will be notes
		if len(optargs) > 0:
			# remaining arguments
			# check for user being pedantic and specificying --notes
			hasNotes = [re.match('--notes', ai) for ai in optargs]
			if any(hasNotes):
				# user gave --notes argument
				# pop full arg off optargs list
				fullarg = optargs.pop([mi is None for mi in hasNotes].index(False))

				# get requested notes
				notes = re.sub('--notes=', '', fullarg)
			else:
				# user did not give notes argument, just let notes be remaining string optargs joined
				idx = [optargs[i] for i, x in enumerate(optargs) if type(x) == str]
				notes = ' '.join(optargs)

		else:
			# no remaining arguments, notes should be empty
			notes = ''

		# return everything
		return rtime, rtag, notes, notice

## pretty printing!
def prettyPrintProject(project, projectName, width=40):
	"""pretty-print the given project"""
	# print the project name
	print('\nproject: {s}'.format(s=projectName))

	# find an appropriate column width, for now just the maximum length of any note for this project
	#inWidth = max(len(project[ti]['innotes']) for ti in project.keys())
	#outWidth = max(len(project[ti]['outnotes']) for ti in project.keys())

	# find the number of rows
	#from math import ceil
	#nrows = ceil(max(len(project[ti][ki]) for ti in project.keys() for ki in ['innotes', 'outnotes']) / width)
	
	# print the column headers
	twidth = 16
	tmwidth = 26
	print(bold + 'tag'.ljust(twidth), 'time in'.ljust(tmwidth), 'in notes'.ljust(width), 'time out'.ljust(tmwidth), 'out notes' + norm.ljust(width))
	
	# print each tag
	keys = [ki for ki in project.keys()]
	for ki in project.keys():
		print(ki.ljust(twidth), project[ki]['in'].ljust(tmwidth), project[ki]['innotes'].ljust(width), str(project[ki]['out']).ljust(tmwidth), 
				project[ki]['outnotes'].ljust(width))
	   # # print tag and in timestamp, no new line
		#print(ki.ljust(width), project[ki]['in'].ljust(width), end='')
		## print as many rows of notes as needed
		#for ri in range(nrows):
			## print innotes
			#print(project[ki]['innotes'][ri * width : min((ri + 1) * width, len(project[ki]['innotes']))].ljust(width), end='')
			## print the out timestamp if on the first row 
			#if ri == 0:
				#print(project[ki]['out'].ljust(width), end='')

			## print the out notes
		  #  print(project[ki]['outnotes'][ri * width : min((ri + 1) * width, len(project[ki]['outnotes']))].ljust(width), end='')
	
	# print each tag
   # from math import ceil
	#for ti in project.keys():
		## find the number of rows this tag will take
		#notes = [project[ti][ki] for ki in ['innotes', 'outnotes']]



