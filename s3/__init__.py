
#
# Super Simple Shell, simple shell application api.
# Copyright (C) 2015  William Palmer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import os
import re
import sys
import cmd
import shlex
import signal
import inspect
import readline
import argparse
import subprocess


readline.set_completer_delims(' ')

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('[shell] %(message)s'))
logger.addHandler(stream_handler)


class ArgShell(object):
    description = 'A basic console application'
    args = {
        # 'name': {
        #     'short': 's',
        #     'long': 'switch'
        #     'toggle': False
        #     'help': 'switch help string',
        #     'default': 'foo, unless specified'
        # }
    }
    def __init__(self):
        parser = argparse.ArgumentParser(
            self.description
        )
        for name, config in self.args.items():
            short = '-{}'.format(
                config.get('short', name[0])
            )
            long = '--{}'.format(
                config.get('long', name.replace('_', '-'))
            )
            toggle = config.get('toggle', False)
            helpstr = config.get('help')
            default = config.get('default', None)
            action = 'store_true' if toggle else 'store'

            parser.add_argument(
                short,
                long,
                dest=name,
                help=helpstr,
                action=action,
                default=default
            )
        self.arguments = parser.parse_args()


class Shell(cmd.Cmd):
    motd = None
    name = 'shell'
    _prompt_ = []
    _shells_ = []
    def __init__(self):
        super(Shell, self).__init__()
        Shell.add(self.name, self)
        if self.motd:
            print(self.motd)
        signal.signal(signal.SIGTERM, self.abort)
        signal.signal(signal.SIGINT, self.abort)
        self.cmdloop()

    @property
    def prompt(self):
        return '.'.join(self._prompt_) + '> '

    @classmethod
    def add(cls, prompt, shell):
        cls._prompt_.append(prompt)
        cls._shells_.append(shell)

    @classmethod
    def remove(cls):
        if len(cls._prompt_):
            _ = cls._prompt_.pop()
            _ = cls._shells_.pop()
        return True

    def abort(self, signal, frame):
        print('exiting the shell')
        self.do_exit([])
        sys.exit(1)

    def parse_args(self, args=''):
        parts = args or []
        if type(args) is str:
            parts = shlex.split(args)
        if len(parts) == 0:
            return (None, None, None)
        cmd = parts.pop(0)
        args = []
        kwargs = {}
        for part in parts:
            if '=' in part and len(part.split('=')) == 2:
                k, v = part.split('=')
                kwargs[k] = v
            else:
                args.append(part)
        if cmd == 'help':
            args = [None]
        return (cmd, args, kwargs)

    def precmd(self, line):
        return shlex.split(line)

    def onecmd(self, args):
        if args:
            raw = ' '.join(args[1:])
            if args[0] == 'help' and len(args) > 1:
                args = args[1:]
                command = getattr(self, 'help_{}'.format(args[0]), None)
                if command:
                    print('\n{}\n'.format(command()))
                return

            cmd, args, kwargs = self.parse_args(args)
            kwargs.update({'raw': raw})
            command = getattr(self, 'do_{}'.format(cmd), None)
            if command:
                try:
                    return command(*args, **kwargs)
                except TypeError as e:
                    logger.info(str(e).split(')')[1])
            else:
                logger.info('invalid command')
        else:
            return False # prevents exit

    def completedefault(self, text, line, start, end):
        cmd, args, kwargs = self.parse_args(line)

        tab_fn = getattr(self, 'tab_{}'.format(cmd))

        if not tab_fn:
            fn = getattr(self, 'do_{}'.format(cmd))
            if fn:
                spec = inspect.getargspec(fn)
                args = spec.args
                if 'self' in args:
                    args.pop(args.index('self'))
                return args
        else:
            return tab_fn(*args, **kwargs)

        return []

    def do_clear(self, *args, **kwargs):
        """clear the console"""
        os.system('clear')

    def do_exit(self, *args, **kwargs):
        """exit the shell"""
        self.remove()
        return True

    def do_quit(self, *args, **kwargs):
        """exit the shell"""
        self.remove()
        return True
