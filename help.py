def printGeneralHelp():
	"""print tman usage, commands, and general options"""
	print('\nusage: tman <command> [options]' + 
	'\n\n' + 
	'commands:\n' + 
	'  help\t\t\tshow detailed help about the given command\n'+
	'  new\t\t\tcreate new timesheet for a project\n'+
	'  in\t\t\tclock in on a project\n'+
	'  out\t\t\tclock out on a project\n'+
	'  tag\t\t\tmanipulate project keyword tags\n'+
	'  list\t\t\tlist projects\n'+
	'  show\t\t\tshow info about a project or the summary file\n'+
	'  search\t\tsearch project files\n'+
	'\n' +
	'general options:\n' + 
	'  -h, --help\t\tshow this help and exit\n' +
	'  -v, --version\t\tprint version information\n')

def printUsage(helpCmd):
	"""print tman command-specific usage"""
	if helpCmd == 'general':
		printGeneralHelp()

	elif helpCmd == 'new':
		print('this should be new help')

	elif helpCmd == 'in':
		print('this should be in help')

	elif helpCmd == 'out':
		print('this should be out help')

	elif helpCmd == 'tag':
		print('this should be tag help')

	elif helpCmd == 'list':
		print('this should be list help')

	elif helpCmd == 'show':
		print('this should be show help')

	elif helpCmd == 'search':
		print('this should be search help')
		
	else: 
		printGeneralHelp()

def printNewHelp():
	"""print detailed help for new command"""
	print('usage: tman new <project> [options]')
