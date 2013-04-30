tman
=====

A simple time management tool.

Overview
--------

`tman` is a simple command-line time management tool. One creates projects and then clock in and 
out as you work to keep track of the time spent on each. The goal of `tman` is to help the user
be more aware of spent actually working on projects.

Usage
-----

You can always type `tman -h` for general information about `tman`, or `tman help <command>` for
more detailed information about a specific command. Usage is probably best shown with a few 
examples. 

To create a new project, use `tman new my-project`. This creates a JSON file with the name
my-project.json, which contains information about the time you spend working on the project. 

To start logging time on this project, write `tman in my-project`.  The command generates a hex 
tag for this particular clock-in event, and associates with it a timestamp. You can control the 
format of the timestamp strings in your tmanrc.

When you're done working on `my-project` simply call `tman out my-project`, which associates 
another timestamp with this event.

You can also add short notes, something like git commit notes, to each clock in or out event, by
calling `tman in my-project notes`. Notes should be a quoted string.

To see a list of all your projects, call `tman list`. This lists the projects, and highlights
whatever project is active with a `<`. To see the history of clock events, you can use `tman
show my-project`.

There are also more advanced options. One example is this. Imagine you're working on `my-project`, 
but then you forget to clock out at the end of the day. To rectify this situation, you can
enforce a particular timestamp by passing the `--time=t` option. `t` can be a relative time. In
this example, if you forgot to clock out, but you finished your work two hours ago, you can write
`tman out my-project --time=-2h`. In general, specifying times in the relative
fashion here, like `-2.5h` or `-2h30m`, should just work. I'm still working to implement more
flexible time specifications, so that you can say things like, `yesterday at 4PM`.

Another option is to pass the `--tag=t` flag. As mentioned above, each clock-in or -out event 
is associated with a hex string "tag". Passing this option applies whatever logging event you'd
like to the event in the project with the given tag. 

Let's see an example. Suppose that you clocked out of a project, and this event was given the tag
`0c22eefac1002b`. Now let's say that you actually kept working on the project for a few more
hours, but forgot to clock back in. You can adjust the clock-out time associated with that
given tag, by calling `tman out my-project --tag=0c22eefac1002b`. This will udpate the clock-out
time to be the current time. You can also specify the time in this case by doing something like
`tman out my-project --tag=0c22eefac1002b --time=-30m`. This updates the clock-out time for the 
event with tag `0c22eefac1002b` to be 30 minutes prior to the current time. 

Since writing project names and long, arbitrary hex tags gets pretty tedious, you can also specify
project names and tags by writing only the first few characters of either one. `tman` will auto-
complete the name if it is uniquely specified, or ask you to pick one if it's not. This will allow
you to update your incorrect clock-out time by calling `tman out my-project --tag=0c2`. Remember
that you can always see the list of clock events by calling `tman show my-project`.

todo
-----
+ [x] nail down basic structure of project JSON structures
+ [x] write commands to create new project file
+ [x] include functionality to apply time/notes updates to individual clock in/out events
+ [x] basic autocomplete of project names and tags
+ [x] functions to list all projects and show project history
+ [ ] functions to search for given keywords
+ [ ] functions to see statistics/summaries for projects
+ [ ] connect these summaries with javascript!
