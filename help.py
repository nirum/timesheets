def printGeneralHelp():
	print('\nusage: tman <command> [options]' + 
	'\n\n' + 
	'commands:\n' + 
	'  help\t\t\tshow detailed help about the given command\n'+
	'  new\t\t\tcreate new timesheet for a project\n'+
	'  in\t\t\tclock in on a project\n'+
	'  out\t\t\tclock out on a project\n'+
	'  tag\t\t\tadd a tag to a project\n'+
	'  list\t\t\tlist projects\n'+
	'  show\t\t\tshow info about a project or the summary file\n'+
	'  search\t\tsearch project files\n'+
	'\n' +
	'general options:\n' + 
	'  -h, --help\t\tshow this help and exit\n' +
	'  -v, --version\t\tprint version information\n')

def printNewUsage():
	print('usage: tman new project/tag')

def printNewHelp():
	print('this should be new help')


