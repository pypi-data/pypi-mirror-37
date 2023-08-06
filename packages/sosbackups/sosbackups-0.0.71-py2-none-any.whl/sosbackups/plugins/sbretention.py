# -*- coding: utf-8 -*-
"""retention plugin"""

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


import glob
import logging
import os
import shutil
import threading
import time

from croniter import croniter
from datetime import datetime
from dwho.classes.plugins import DWhoPluginBase, PLUGINS
from sonicprobe.libs import workerpool


LOG                 = logging.getLogger('sosbackups.plugins.retention')
_KILLED             = False
WORKER_LIFETIME     = 300
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_MAX_DAYS    = 40
MAX_RETENTION_UNITS =  {'d': 1,
                        'm': 30,
                        'y': 365}


class SosBackupsRetentionClean(threading.Thread):
    def __init__(self, name, xpath, options = None):
        threading.Thread.__init__(self)

        self.name    = name
        self.xpath   = xpath
        self.options = options

    def _parsing_max(self, max_days):
        if isinstance(max_days, (int, float, long)):
            return long(max_days)

        if not max_days:
            return DEFAULT_MAX_DAYS

        if not isinstance(max_days, basestring):
            LOG.error("invalid max retention: %r", max_days)
            return DEFAULT_MAX_DAYS

        if max_days.isdigit():
            return long(max_days)

        unit = max_days[-1].lower()
        if unit not in MAX_RETENTION_UNITS:
            LOG.error("invalid max retention unit: %r", max_days)
            return DEFAULT_MAX_DAYS

        max_days = max_days[:-1]
        if not max_days.isdigit():
            LOG.error("invalid max retention days: %r", max_days)
            return DEFAULT_MAX_DAYS

        return long(max_days) * MAX_RETENTION_UNITS[unit]

    def _delete_directory(self, dirpath, date_format, max_days):
        for x in os.listdir(dirpath):
            d = os.path.join(dirpath, x)
            if not os.path.isdir(d):
                continue

            try:
                dirdate = datetime.strptime(x, date_format)
            except ValueError:
                LOG.error("unable to parse directory date: %r. (date_format: %r)",
                          d,
                          date_format)
                continue

            nb_days = (datetime.now() - dirdate).days
            if nb_days >= max_days:
                LOG.info("removing directory: %r. (nb_days: %d, max_days: %d)",
                         d,
                         nb_days,
                         max_days)
                shutil.rmtree(d)

    def run(self):
        options     = self.options.copy()
        date_format = options.get('date_format') or '%Y-%m-%d'
        max_days    = self._parsing_max(options.get('max'))
        is_glob     = options.get('glob')
        fkwargs     = {'env': os.environ,
                       'gmtime': datetime.utcnow(),
                       'time': datetime.now(),
                       'vars': options.get('vars') or {}}

        dirpath     = self.xpath.format(**fkwargs)

        if is_glob:
            for x in glob.iglob(dirpath):
                self._delete_directory(x, date_format, max_days)
        elif os.path.isdir(dirpath):
            self._delete_directory(dirpath, date_format, max_days)

        return self.name

    def __call__(self):
        try:
            self.run()
        except Exception, e:
            LOG.exception(e)
        finally:
            return self.name


class SosBackupsCronRetentionThread(threading.Thread):
    def __init__(self, cron_pool, tabs):
        threading.Thread.__init__(self)
        self.cron_pool = cron_pool
        self.tabs      = tabs
        self.runners   = []
        self.history   = {}

    def callback(self, name):
        if name in self.runners:
            self.runners.remove(name)

    def run(self):
        while not _KILLED:
            for tab, paths in self.tabs.iteritems():
                x = paths
                if isinstance(paths, basestring):
                    x = [{'path_format': paths}]

                for params in x:
                    options = params.copy()
                    xpath   = os.path.abspath(options.pop('path_format'))
                    name    = "%s:%s" % (tab, xpath)

                    if name not in self.history:
                        self.history[name] = []

                    if name in self.runners:
                        continue

                    t = datetime.now().strftime('%Y-%m-%d %H:%M')

                    if t in self.history[name]:
                        if len(self.history[name]) > 120:
                            del self.history[name][0:120]
                        continue

                    self.history[name].append(t)

                    i = croniter(tab, datetime.now())
                    p = i.get_prev(datetime).strftime('%Y-%m-%d %H:%M')
                    n = i.get_next(datetime).strftime('%Y-%m-%d %H:%M')

                    if t in (p, n):
                        self.runners.append(name)
                        self.cron_pool.run(SosBackupsRetentionClean(name, xpath, options), self.callback)

            time.sleep(1)


class SosBackupsRetentionPlugin(DWhoPluginBase):
    PLUGIN_NAME = 'retention'

    def safe_init(self):
        self.tabs      = self.plugconf['tabs']
        self.cron_pool = workerpool.WorkerPool(max_workers = int(self.plugconf.get('max_workers') or 1),
                                               life_time   = self.plugconf.get('worker_lifetime', WORKER_LIFETIME),
                                               name        = 'cron_pool')
        self.cron_sync = SosBackupsCronRetentionThread(self.cron_pool, self.tabs)
        self.cron_sync.daemon = True

    def at_start(self):
        self.cron_sync.start()

    def at_stop(self):
        global _KILLED
        _KILLED = True

        if self.cron_pool:
            self.cron_pool.killall(1)


if __name__ != "__main__":
    def _start():
        PLUGINS.register(SosBackupsRetentionPlugin())
    _start()
