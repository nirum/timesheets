import os, json

def getTmanPrefs(fid):
	"""read tman.conf preferences file"""
	with fid as file:
		prefs = [line.rstrip() for line in file]

	return prefs

def makeProjectFilename(prefs, projectName):
	"""make a full filename for the given project"""
	return os.path.join(os.path.expanduser(prefs[0]), 'projects', projectName + '.json')

def createNewProject(prefs, projectName):
	"""create a new project with the given name"""
	print('creating new project "' + projectName + '"')
	project = {
			'metadata': {'name': projectName,
						 'file': makeProjectFilename(prefs, projectName),
						 'active': False}, 
			'timestamps': [{'in': [], 
							'out': [], 
							'notes': []}]}
	return project

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
		project = json.load(makeProjectFilename(prefs, projectName))

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
