Super Simple Shell - s3
=======================

S3 attempts to simplify building shell applications with Python's cmd module.

## Requirements

* python 3.4

## Installation

`git clone https://github.com/w-p/super-simple-shell.git`

`cd super-simple-shell`

`pip install .`

## Overview

### Creating a command line application
* subclass s3.ArgShell
* give it some arguments
* instantiate it
* access the resulting arguments

### Adding Arguments
Arguments are provided in the form of a dictionary where the key is the argument name and the value is another dictionary populated with the argument's configuration. So:

    args = {
        'myfirstarg': {
            'help': 'no short or long set, call me with -m or --myfirstarg',
            'default': 'foo'
        },
        'mysecondarg': {
            'short': 'a',
            'long': 'my-second-arg',
            'help': 'short and long set, call me with -a or --my-second-arg',
            'default': 'bar'
        },
        'myswitch': {
            'short': 's',
            'toggle': True,
            'help': 'only short is set, call me with -s or --myswitch',
            'default': False
        }
    }

Command line switches are generated from the name of the argument using the first letter of the key and the key itself. The optional `short` and `long` values are used only when defined. This helps avoid argument name conflicts.

### Usage Example

    #! /usr/bin/env python3
    import s3
    from datetime import datetime

    class Simple(s3.ArgShell):
        description = 'A simple command-line application'
        args = {
            'hello': {'short': 'H', 'help': 'Say hello', 'default': 'John Doe'},
            'greet': {'toggle': True, 'help': 'Print a greeting'}
        }

        def hello(self, value):
            print('Hello, {}.'.format(value))

        def greet(self):
            now = datetime.now()
            time = now.strftime('%H:%M')
            phase = 'evening'
            if now.hour < 12:
                phase = 'morning'
            elif now.hour < 18:
                phase = 'afternoon'
            print('Good {}, the time is {}'.format(phase, time))


    if __name__ == '__main__':
        cmd = Simple()
        if cmd.arguments.hello:
            cmd.hello(cmd.arguments.hello)
        if cmd.arguments.greet:
            cmd.greet()

For the above, save it (as 'simple'), chmod it, and run it. You'll see:

    $ ./simple
    Hello, John Doe.

To see what you can do:

    $ ./simple --help
    usage: A simple command-line application [-h] [-g] [-H HELLO]

    optional arguments:
      -h, --help            show this help message and exit
      -g, --greet           Print a greeting
      -H HELLO, --hello HELLO
                            Say hello

To use it:

    $ ./simple --hello $USER -g
    Hello, will.
    Good morning, the time is 09:39

_____
### Creating a shell
* subclass `s3.Shell`
* give it something to do
* give it some tab completions
* give it some help
* instantiate it
* call `run()`

### Included Shell Commands:
  * `clear`: Clears the console
  * `quit`: Exits the current shell
  * `exit`: Exits the current shell

### Signal Handlers:
  * `SIGTERM`: Forceful exit, bound to `ctrl-c`
  * `SIGINT`: Forceful exit, bound to `ctrl-c`

### Anatomy of a shell:
A shell consists of an `motd`, a `name`, and a series of commands such that:

* Specifying an `motd` prints a message when the shell starts.
* Specifying a `name` replaces the default prompt of `shell>`.
* Nest shells by instantiating an `s3.Shell` object within a command.
* If a command returns `True`, the shell will exit.
* If `ctrl-c` is pressed, the shell will forcefully exit.

### Anatomy of a shell command:
A command consists of the command's work, it's help, and it's tab completions. Implementing help and tab completions is optional.

To clarify:
* A function of `do_something` exposes the `something` command.
* A function of `help_something` exposes the `help something` command.
* A function of `tab_something` exposes `help <tab><tab>` functionality.
* Help functions should return a string. Printing is handled by s3.

### Usage Example


    #! /usr/bin/env python3
    import s3

    class Simple(s3.Shell):
        motd = """
        Welcome to the Simple Command Shell
        """
        name = 'scs'

        def do_hello(self, name):
            print('Hello, {}.'.format(name))

        def tab_hello(self, text):
            names = ['John', 'Sam', 'Jennifer', 'Sarah']
            return [n for n in names if text.lower() in n.lower()]

        def help_hello(self):
            return (
                'hello <name>\n' +
                'Says hello to a given name.'
            )

    if __name__ == '__main__':
        Simple().run()

For the above, save it, chmod it, and run it. You'll see:

        Welcome to the Simple Command Shell

    scs>

To see what you can do:

    scs> help

    Documented commands (type help <topic>):
    ========================================
    clear  exit  hello  help  quit

    scs>

To see what a documented command does:

    scs> help hello

    hello <name>
    Says hello to a given name.

    scs>

To see tab completions, begin typing an argument and press `tab`:

    scs> hello J
    Jennifer  John
    scs>

To use a command:

    scs> hello John
    Hello, John.
    scs>

To exit the shell, use exit or quit:

    scs> quit

To force the shell to exit, use `ctrl-c`:

    scs> exiting the shell
