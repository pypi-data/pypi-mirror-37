# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback
import uuid

from macdaily.cli.update import parse_args
from macdaily.cls.update.apm import ApmUpdate
from macdaily.cls.update.brew import BrewUpdate
from macdaily.cls.update.cask import CaskUpdate
from macdaily.cls.update.gem import GemUpdate
from macdaily.cls.update.mas import MasUpdate
from macdaily.cls.update.npm import NpmUpdate
from macdaily.cls.update.pip import PipUpdate
from macdaily.cls.update.system import SystemUpdate
from macdaily.cmd.config import parse_config
from macdaily.util.const import (__version__, bold, green, pink, purple, red,
                                 reset, under, yellow)
from macdaily.util.misc import make_description, print_misc, print_text, record

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


def update(argv=None):
    # parse args & config
    args = parse_args(argv)
    config = parse_config()

    # context redirection flags
    quiet = args.quiet
    verbose = args.quiet and (not args.verbose)

    # fetch current time
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    logtime = datetime.date.strftime(today, r'%H%M%S')

    # mkdir for logs
    logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'update', logdate))
    logpath.mkdir(parents=True, exist_ok=True)

    # prepare command paras
    filename = os.path.join(logpath, '{}-{!s}.log'.format(logtime, uuid.uuid4()))
    timeout = config['Miscellanea']['timeout']
    askpass = config['Miscellanea']['askpass']
    disk_dir = config['Path']['arcdir']
    brew_renew = None

    # record program status
    text = '{}{}|🚨|{} {}Running MacDaily version {}{}'.format(bold, green, reset, bold, __version__, reset)
    print_text(text, filename, redirect=quiet)
    record(filename, args, today, config, redirect=verbose)

    cmd_list = list()
    for mode in {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}:
        # skip disabled commands
        if (not config['Mode'].get(mode, False)) or getattr(args, 'no_{}'.format(mode), False):
            text = 'macdaily-update: {}{}{}: command disabled'.format(yellow, mode, reset)
            print_text(text, filename, redirect=verbose)
            continue

        # update package specifications
        packages = getattr(args, '{}_pkgs'.format(mode), list())
        namespace = getattr(args, mode, dict())
        if not (packages or namespace or args.all):
            text = 'macdaily-update: {}{}{}: nothing to upgrade'.format(yellow, mode, reset)
            print_text(text, filename, redirect=verbose)
            continue
        namespace['packages'].extend(packages)

        # run command
        cmd_cls = globals()['{}Update'.format(mode.capitalize())]
        command = cmd_cls(namespace, filename, timeout, askpass, disk_dir, brew_renew)

        # record command
        cmd_list.append(command)
        brew_renew = command.time

    text = '{}{}|📖|{} {}MacDaily report of update command{}'.format(bold, green, reset, bold, reset)
    print_text(text, filename, redirect=quiet)

    for command in cmd_list:
        desc = make_description(command)
        pkgs = '{}{}, {}'.format(reset, bold, green).join(command.packages)
        miss = '{}{}, {}'.format(reset, bold, yellow).join(command.notfound)
        ilst = '{}{}, {}'.format(reset, bold, pink).join(command.ignored)
        fail = '{}{}, {}'.format(reset, bold, red).join(command.failed)

        if pkgs:
            flag = (len(pkgs) == 1)
            text = 'Upgraded following {}{}{}{}: {}{}{}'.format(under, desc(flag), reset, bold, green, pkgs, reset)
        else:
            text = 'No {}{}{}{} upgraded'.format(under, desc(False), reset, bold)
        print_misc(text, filename)

        if fail:
            flag = (len(fail) == 1)
            text = 'Upgrade of following {}{}{}{} failed: {}{}{}'.format(under, desc(flag), reset, bold, red, fail, reset)
        else:
            verb, noun = ('s', '') if len(fail) == 1 else ('', 's')
            text = 'All {}{}{}{} upgrade{} succeed{}'.format(under, desc(False), reset, bold, noun, verb)
        print_misc(text, filename, redirect=verbose)

        if ilst:
            flag = (len(ilst) == 1)
            text = 'Ignored updates of following {}{}{}{}: {}{}{}'.format(under, desc(flag), reset, bold, pink, ilst, reset)
        else:
            text = 'No {}{}{}{} ignored'.format(under, desc(False), reset, bold)
        print_misc(text, filename, redirect=verbose)

        if miss:
            flag = (len(miss) == 1)
            text = 'Following {}{}{}{} not found: {}{}{}'.format(under, desc(flag), reset, bold, yellow, miss, reset)
        else:
            text = 'Hit all {}{}{}{} specifications'.format(under, desc(False), reset, bold)
        print_misc(text, filename, redirect=verbose)

    if len(cmd_list) == 0:
        text = 'macdaily: {}update{}: no packages upgraded'.format(purple, reset)
        print_text(text, filename, redirect=verbose)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print('macdaily: {}update{}: cannot show log file {!r}'.format(red, reset, filename), file=sys.stderr)

    mode_lst = [command.mode for command in cmd_list]
    mode_str = ', '.join(mode_lst) if mode_lst else 'null'
    text = ('{}{}|🍺|{} {}MacDaily successfully performed update process '
            'for {} package managers{}'.format(bold, green, reset, bold, mode_str, reset))
    print_text(text, filename, redirect=quiet)


if __name__ == '__main__':
    sys.exit(update())
