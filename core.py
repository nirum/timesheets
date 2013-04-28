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
	# notify
	print('creating new project "' + projectName + '"')

	# create an empty project dict
	project = {'in': [], 
			   'out': [],
			   'notes': []}

	# add the project to the metadata file
	addProjectToMd(prefs, projectName)

	return project

def makeTimestamp(prefs):
	"""return a string timestamp according to the user's preferred format"""
	return time.strftime(prefs['timefmt'])

def clockIn(prefs, projectName, project, t, notes):
	"""clock in on a project"""
	# set the in timestamp
	project['in'].append(t)
	# set the out timestamp to zero for now
	project['out'].append(0)
	# append the optional notes
	project['notes'].append(notes)

	# set the project as active
	setActive(prefs, projectName)

def clockOut(prefs, projectName, project, t, notes):
	"""clock out on a project"""
	# set the timestamp
	project['out'][-1] = t

	# append notes
	project['notes'].append(notes)

	# set project as inactive
	setInactive(prefs)

def activeProject(prefs):
	"""return the currently active project"""
	# read metadata.json
	md = readMetadata(prefs)

	# check if project is active
	return md['active']


def setActive(prefs, projectName):
	"""set a project as active"""
	# read current metadata
	md = readMetadata(prefs)

	# list the current project as active
	md['active'] = projectName

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
	

def saveProject(prefs, projectName, project):
	"""save a project to its file"""
	# open the file
	fid = open(os.path.join(os.path.expanduser(prefs['tmandir']), 'projects', projectName + '.json'), 'w')
	json.dump(project, fid)
	fid.close()

def loadProject(prefs, projectName):
	"""load the JSON project object with the given name"""
	e = checkProjectExists(prefs, projectName)
	if e:
		fid = open(os.path.join(os.path.expanduser(prefs['tmandir']), 'projects', projectName + '.json'), 'r')
		project = json.load(fid)
		fid.close()
	else:
		project = None

	return project

def getTimestamps(project):
	return project['timestamps']

def checkProjectExists(prefs, projectName):
	"""check if a project file exists"""
	# read metadata JSON file
	md = readMetadata(prefs)

	# return if the project is listed in metadata
	return projectName in md['projects']

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
