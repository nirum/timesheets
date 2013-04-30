# define bold, underline, normal text for pretty printing
bold = '\033[1m'
under = '\033[4m'
norm = '\033[0m'

def printGeneralHelp():
	"""print tman usage, commands, and general options"""
	print('\nusage: tman <command> <project> [options]' +
	'\n\n' +
	'commands:\n' +
	'  help\t\t\tshow detailed help about the given command\n'+
	'  new\t\t\tcreate new timesheet for a project\n'+
	'  rm\t\t\tremove a timesheet for a project\n' + 
	'  in\t\t\tclock in on a project\n'+
	'  out\t\t\tclock out on a project\n'+
	'  list\t\t\tlist projects\n'+
	'  show\t\t\tshow info about a project or the summary file\n'+
	'  search\t\tsearch project files\n'+
	'\n' +
	'general:\n' +
	'  -h, --help\t\tshow this help and exit\n' +
	'  -v, --version\t\tprint version information\n')

def printSetupHelp():
	"""print help for setting up tman"""
	print('Welcome to tman, a simple time management system.')
	print('Nothing is currently setup, but we can change that very quickly')
	print('Running tmansetup.sh will run you through the simple setup procedure')

def printUsage(helpCmd):
	"""print tman command-specific usage"""
	if helpCmd == 'general':
		printGeneralHelp()

	elif helpCmd == 'new':
		printNewHelp()

	elif helpCmd == 'rm':
		printRmHelp()

	elif helpCmd == 'in':
		printInHelp()

	elif helpCmd == 'out':
		printOutHelp()

	elif helpCmd == 'list':
		printListHelp()

	elif helpCmd == 'show':
		printShowHelp()

	elif helpCmd == 'search':
		print('this function is not yet supported')

	else:
		printGeneralHelp()

def printNewHelp():
	"""print detailed help for new command"""
	print('\nusage: tman new <{u}project{n}>\n'.format(u=under, n=norm))
	print('create a new timesheet for the given {u}project{n}\n'.format(u=under, n=norm))

def printRmHelp():
	"""print detailed help for the rm command"""
	print('\nusage: tman rm [{b}-f{n}] {u}project{n} [{b}--tag{n}={u}t{n}]'.format(b=bold, u=under, n=norm))
	print('\nremove projects or clock in/out events\n')
	print('  OPTIONS:\n\n\
	{b}-f{n}\n\
	  Force the removal without asking for verification\n\n\
	{b}--tag{n}={u}t{n}\n\
	  Remove the clock in/out event with tag {u}t{n} from the requested {u}project{n}.\n\
	  {u}t{n}can be either a full project tag or a substring. In the event that there is a\n\
	  single match, it will be autocompleted and a notification will be printed. In the case\n\
	  of multiple possible matches, you will be asked to pick one.\n'.format(b=bold, u=under, n=norm))

def printInHelp():
	"""print detailed help for in command"""
	print('\nusage: tman in {u}project{n} [{b}--time{n}={u}t{n}] [{b}--tag{n}={u}t{n}] [[{b}--notes{n}=]{u}notes{n}]'.format(b=bold, u=under, n=norm))
	print('\nclock in on the requested {u}project{n}\n'.format(u=under, n=norm))
	print('  OPTIONS:\n\n\
	{b}--time{n}={u}t{n}\n\
	  Force using a clock-in time of {u}t{n}. This can be useful when one forgets\n\
	  to clock in on a given project, as this option can be used to simulate\n\
	  the desired clock in time. {u}t{n} can be specified in a number of ways. For\n\
	  example, it may be expressed as a relative time, such as "-1d" or "-3h30m".\n\
	  It may also be expressed as "yesterday at 13:30", so long as it is entirely \n\
 	  enclosed within quotes. {u}t{n} can also be expressed as a true timestamp. {b}tman{n} \n\
	  will do its best to determine the correct time.\n\n\
	{b}--tag{n}={u}t{n}\n\
	  Apply the clock in time directly to the event with tag {u}t{n} for the given\n\
	  project. This is useful for manipulating past clock in events, such as \n\
	  adding or removing time. For example, if one mistakenly clocks in on a \n\
	  project, use `tman list <project>` to see the tags for the offending clock \n\
	  in event. This tag (or any substring sufficient to uniquely identify it) \n\
	  may be passed as in {b}--tag{n}={u}t{n} to adjust the clock in event. This option\n\
	  may be combined with the {b}--time{n} option to specify an event and time.\n\n\
	[[{b}--notes{n}]={u}notes{n}]\n\
	  Add notes to your clock in timestamp, for example, to indicate what you intend\n\
	  to work on during the next time period. {u}notes{n} should be contained entirely \n\
	  within quotes, but need not be specified with the {b}--notes{n} parameter\n'.format(b=bold, n=norm, u=under))

def printOutHelp():
	"""print detailed help for out command"""
	print('\nusage: tman out {u}project{n} [{b}--time{n}={u}t{n}] [{b}--tag{n}={u}t{n}] [[{b}--notes{n}=]{u}notes{n}]'.format(b=bold, u=under, n=norm))
	print('\nclock out on the requested {u}project{n}\n'.format(u=under, n=norm))
	print('  OPTIONS:\n\n\
	{b}--time{n}={u}t{n}\n\
	  Force using a clock-out time of {u}t{n}. This can be useful when one forgets\n\
	  to clock out on a given project, as this option can be used to simulate\n\
	  the desired clock out time. {u}t{n} can be specified out a number of ways. For\n\
	  example, it may be expressed as a relative time, such as "-1d" or "-3h30m".\n\
	  It may also be expressed as "yesterday at 13:30", so long as it is entirely \n\
 	  enclosed within quotes. {u}t{n} can also be expressed as a true timestamp. {b}tman{n} \n\
	  will do its best to determine the correct time.\n\n\
	{b}--tag{n}={u}t{n}\n\
	  Apply the clock out time directly to the event with tag {u}t{n} for the given\n\
	  project. This is useful for manipulating past clock out events, such as \n\
	  adding or removing time. For example, if one mistakenly clocks out on a \n\
	  project, use `tman list <project>` to see the tags for the offending clock \n\
	  out event. This tag (or any substring sufficient to uniquely identify it) \n\
	  may be passed as in {b}--tag{n}={u}t{n} to adjust the clock out event. This option\n\
	  may be combined with the {b}--time{n} option to specify an event and time.\n\n\
	[[{b}--notes{n}]={u}notes{n}]\n\
	  Add notes to your clock out timestamp, for example, to indicate what you intend\n\
	  to work on during the next time period. {u}notes{n} should be contained entirely \n\
	  within quotes, but need not be specified with the {b}--notes{n} parameter\n'.format(b=bold, n=norm, u=under))

def printListHelp():
	"""print help for list command"""
	print('\nusage: tman list\n')
	print('show all current projects\n')

def printShowHelp():
	"""print help for show command"""
	print('\nusage: tman show {u}project{n}'.format(u=under, n=norm))
	print('\nshow the clock in/out history for the requested {u}project{n}\n'.format(u=under, n=norm))
