# -*- coding: utf-8 -*-
"""copy plugin"""

__author__  = "Adrien DELLE CAVE"
__license__ = """
    Copyright (C) 2018  doowan

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""

import datetime
import logging
import os

from dwho.classes.inoplugs import INOPLUGS
from sosbackups.classes.rsyncplug import SosBackupsRsyncPlug


LOG = logging.getLogger('sosbackups.plugins.copy')


class SosBackupsCopyInoPlug(SosBackupsRsyncPlug):
    PLUGIN_NAME = 'copy'

    def run(self):
        if not self.plugconf:
            return

        params         = self.plugconf.copy()
        prefix_path    = params.get('prefix_path') or self.prefix_path

        path_format    = params.get('path_format') or '{dest}'
        fkwargs        = {'dest': self.realdstpath(self.event, self.filepath, prefix_path),
                          'filepath': self.filepath,
                          'dirname': os.path.dirname(self.filepath),
                          'filename': os.path.basename(self.filepath),
                          'env': os.environ,
                          'gmtime': datetime.datetime.utcnow(),
                          'time': datetime.datetime.now(),
                          'vars': params.get('vars') or {}}

        eparams        = self.get_event_params()

        if 'vars' in eparams:
            fkwargs['vars'].update(eparams['vars'] or {})

        if eparams.get('__time__'):
            fkwargs['time'] = eparams['__time__']

        if eparams.get('__gmtime__'):
            fkwargs['gmtime'] = eparams['__gmtime__']

        if 'notifications' in eparams:
            params['notifications'] = bool(eparams['notifications'])

        path_options   = self._get_path_options()
        if path_options:
            if path_options.get('path_format'):
                path_format = path_options['path_format']

            if path_options.get('args'):
                fkwargs.update(path_options.get('args'))

        params['dest'] = path_format.format(**fkwargs)

        self.try_exec_rsync(params, self.filepath)


if __name__ != "__main__":
    def _start():
        INOPLUGS.register(SosBackupsCopyInoPlug())
    _start()
