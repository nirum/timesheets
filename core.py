import os, json, time

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

def makeProjectFilename(prefs, projectName):
	"""make a full filename for the given project"""
	return os.path.join(os.path.expanduser(prefs['tmandir']), 'projects', projectName + '.json')

def createNewProject(prefs, projectName):
	"""create a new project with the given name"""
	print('creating new project "' + projectName + '"')
	project = {
			'metadata': {'name': projectName,
						 'file': makeProjectFilename(prefs, projectName),
						 'active': False}, 
			'timestamps': []}
			#timestamps': [{'in': [], 
							#'out': [], 
							#'notes': []}]}
	return project

def makeTimestamp(prefs):
	"""return a string timestamp according to the user's preferred format"""
	return time.strftime(prefs['timefmt'])

def clockIn(prefs, project, t, notes):
	"""clock in on a project"""
	# set the timestamp
	project['timestamps'].append({'in': t, 
		'out': 0, 'notes': [notes]})

	# set the project as active
	setActive(project)

def clockOut(prefs, project, t, notes):
	"""clock out on a project"""
	# set the timestamp
	project['timestamps'][-1]['out'] = t

	# append notes
	project['timestamps'][-1]['notes'].append(notes)

	# set project as inactive
	setInactive(project)

def isActive(project):
	"""determine if we've clocked in on the project"""
	return project['metadata']['active']
	

def setActive(project):
	"""set a project as active"""
	project['metadata']['active'] = True

def setInactive(project):
	"""set a project as inactive"""
	project['metadata']['active'] = False

def saveProject(project):
	"""save a project to its file"""
	# open the file
	fid = open(getProjectFilename(project), 'w')
	json.dump(project, fid)
	fid.close()

def loadProject(prefs, projectName):
	"""load the JSON project object with the given name"""
	fname = makeProjectFilename(prefs, projectName)
	e = checkProjectExists(fname)
	if e:
		fid = open(fname, 'r')
		project = json.load(fid)
		fid.close()
	else:
		project = None

	return project

def getProjectName(project):
	"""get the project's name from its metadata"""
	return project['metadata']['name']

def getProjectFilename(project):
	"""make the full path to the project JSON file"""
	return project['metadata']['file']

def getTimestamps(project):
	return project['timestamps']

def checkProjectExists(fname):
	"""check if a project file exists"""
	return os.path.isfile(fname)
