Super Simple Shell - s3
=======================

S3 is attempts to simplify building shell applications with Python's cmd module.

Requirements
------------
* python 3.4

Installation
------------

`git clone https://github.com/w-p/super-simple-shell.git`

`cd super-simple-shell`

`pip install .`

Overview
--------

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

Usage Example
-------------


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
