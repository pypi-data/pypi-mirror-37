# -*- coding: utf-8 -*-

import shutil
import sys

from macdaily.cls.command import Command
from macdaily.util.const import bold, flash, red, red_bg, reset
from macdaily.util.misc import print_text


class MasCommand(Command):

    @property
    def mode(self):
        return 'mas'

    @property
    def name(self):
        return 'Mac App Store CLI'

    @property
    def desc(self):
        return ('macOS application', 'macOS applications')

    def _check_exec(self):
        self.__exec_path = shutil.which('mas')
        flag = (self.__exec_path is None)
        if flag:
            print('macdaily-update: {}{}mas{}: command not found'.format(red_bg, flash, reset), file=sys.stderr)
            text = ('macdaily-update: {}mas{}: you may download MAS through following command -- '
                    "`{}brew install mas{}'".format(red, reset, bold, reset))
            print_text(text, self._file, redirect=self._qflag)
        return flag

    def _loc_exec(self):
        self._exec = {self.__exec_path}
        del self.__exec_path
