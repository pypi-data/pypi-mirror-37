# -*- coding: utf-8 -*-

import contextlib
import datetime
import functools
import getpass
import os
import platform
import re
import sys

import ptyng

from macdaily.util.const import (SHELL, blue, bold, grey, program, purple,
                                 python, red, reset)
from macdaily.util.error import UnsupportedOS


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() != 'Darwin':
            raise UnsupportedOS('macdaily: error: script runs only on macOS')
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('macdaily: {}error{}: operation interrupted'.format(red, reset), file=sys.stderr)
            raise
    return wrapper


def date():
    now = datetime.datetime.now()
    txt = datetime.datetime.strftime(now, '%+')
    return txt


def make_context(devnull, redirect=False):
    if redirect:
        return contextlib.redirect_stdout(devnull)
    return contextlib.nullcontext()


def make_description(command):
    def desc(singular):
        if singular:
            return command.desc[0]
        else:
            return command.desc[1]
    return desc


def print_info(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', '{}{}|💼|{} {}{}{}'.format(bold, blue, reset, bold, text, reset)], file)


def print_misc(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', '{}{}|📌|{} {}{}{}'.format(bold, grey, reset, bold, text, reset)], file)


def print_scpt(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', '{}{}|📜|{} {}{}{}'.format(bold, purple, reset, bold, text, reset)], file)


def print_text(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', text], file)


def record(file, args, today, config, redirect=False):
    # record program arguments
    print_misc('{} {}'.format(python, program), file, redirect)
    with open(file, 'a') as log:
        log.writelines(['TIME: {!s}\n'.format(today), 'FILE: {}\n'.format(file)])

    # record parsed arguments
    print_misc('Parsing command line arguments'.format(), file, redirect)
    with open(file, 'a') as log:
        for key, value in vars(args).items():
            if isinstance(value, dict):
                for k, v, in value.items():
                    log.write('ARG: {} -> {} = {}\n'.format(key, k, v))
            else:
                log.write('ARG: {} = {}\n'.format(key, value))

    # record parsed configuration
    print_misc('Parsing configuration file '
               '{!r}'.format(os.path.expanduser("~/.dailyrc")), file, redirect)
    with open(file, 'a') as log:
        for key, value in config.items():
            for k, v, in value.items():
                log.write('CFG: {} -> {} = {}\n'.format(key, k, v))


def run(argv, file, *, redirect=False, timeout=None, shell=False, executable=None):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            return script(argv, file, timeout=timeout, shell=shell, executable=executable)


def script(argv=SHELL, file='typescript', *, timeout=None, shell=False, executable=None):
    if isinstance(argv, str):
        argv = [argv]
    else:
        argv = list(argv)
    if shell:
        argv = [SHELL, '-c'] + argv
    if executable:
        argv[0] = executable

    def master_read(fd):
        data = os.read(fd, 1024)
        text = re.sub(rb'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', rb'', data, flags=re.IGNORECASE)
        typescript.write(text)
        return data

    with open(file, 'a') as typescript:
        typescript.write('Script started on {}\n'.format(date()))
        typescript.write('command: {!r}\n'.format(" ".join(argv)))
    with open(file, 'ab') as typescript:
        returncode = ptyng.spawn(argv, master_read, timeout=timeout)
    with open(file, 'a') as typescript:
        typescript.write('Script done on {}\n'.format(date()))
    return returncode


def sudo(argv, file, *, askpass=None, sethome=False, redirect=False, timeout=None, executable=None):
    def make_command():
        if not isinstance(argv, str):
            argv = ' '.join(argv)
        if getpass.getuser() == 'root':
            return argv
        sudo_askpass = '' if askpass is None else 'SUDO_ASKPASS={!r} '.format(askpass)
        set_home = ' --set-home' if sethome else ''
        return '{}sudo --askpass{} {}'.format(sudo_askpass, set_home, argv)
    return run(make_command(), file, redirect=redirect, timeout=timeout, shell=True, executable=executable)
