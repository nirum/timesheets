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
	'general:\n' +
	'  -h, --help\t\tshow this help and exit\n' +
	'  -v, --version\t\tprint version information\n')

def printUsage(helpCmd):
	"""print tman command-specific usage"""
	if helpCmd == 'general':
		printGeneralHelp()

	elif helpCmd == 'new':
		printNewHelp()

	elif helpCmd == 'in':
		printInHelp()

	elif helpCmd == 'out':
		printOutHelp()

	elif helpCmd == 'tag':
		print('this should be tag help')

	elif helpCmd == 'list':
		printListHelp()

	elif helpCmd == 'show':
		print('this should be show help')

	elif helpCmd == 'search':
		print('this should be search help')

	else:
		printGeneralHelp()

def printNewHelp():
	"""print detailed help for new command"""
	print('usage: tman new <project>')
	print('create a new project with the given name')

def printInHelp():
	"""print detailed help for in command"""
	print('usage: tman in <project> [notes]')
	print('clock in on the requested project, optionally adding notes when you do so')

def printOutHelp():
	"""print detailed help for out command"""
	print('usage: tman out <project> [notes]')
	print('clock out on the requested project, optionally adding notes when you do so')

def printListHelp():
	"""print help for list command"""
	print('usage: tman list')
	print('show all current projects')
