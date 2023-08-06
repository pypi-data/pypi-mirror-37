# -*- coding: utf-8 -*-
"""push plugin"""

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

import logging
import os

from dwho.classes.inoplugs import INOPLUGS
from sosbackups.classes.rsyncplug import SosBackupsRsyncPlug


LOG = logging.getLogger('sosbackups.plugins.push')


class SosBackupsPushInoPlug(SosBackupsRsyncPlug):
    PLUGIN_NAME = 'push'

    def run(self):
        if not self.plugconf:
            return

        if not isinstance(self.plugconf, dict) \
           or not self.plugconf.get('hosts'):
            LOG.info("missing hosts")
            return

        eparams = self.get_event_params()

        for name, opts in self.plugconf['hosts'].iteritems():
            if not opts.get('host'):
                opts['host'] = name

            params = eparams.copy()
            params.update(opts)

            self.try_exec_rsync(params, self.filepath)


if __name__ != "__main__":
    def _start():
        INOPLUGS.register(SosBackupsPushInoPlug())
    _start()
