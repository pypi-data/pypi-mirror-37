# -*- coding: utf-8 -*-
"""cronsync plugin"""

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


import copy
import datetime
import hashlib
import logging
import os
import pyinotify
import re
import threading
import time
import traceback
import uuid

from croniter import croniter
from dwho.classes.errors import DWhoConfigurationError
from dwho.classes.inotify import DWhoInotifyEventHandler
from dwho.classes.notifiers import DWhoPushNotifications
from dwho.classes.plugins import DWhoPluginBase, PLUGINS
from dwho.config import DWHO_SHARED
from sonicprobe import helpers
from sonicprobe.libs import workerpool


LOG               = logging.getLogger('sosbackups.plugins.cronsync')
DATE_FORMAT       = '%Y-%m-%d %H:%M:%S'
DEFAULT_STATS     = {'dirs': {'success': 0, 'failure': 0, 'size': 0, 'sum': 0},
                     'files': {'success': 0, 'failure': 0, 'size': 0, 'sum': 0},
                     'total': {'success': 0, 'failure': 0, 'size': 0, 'sum': 0}}
WORKER_LIFETIME   = 3600
_CRON_DATE_FORMAT = '%Y-%m-%d %H:%M'
_KILLED           = False


class SosBackupsScanEvent(object):
    def __init__(self, pathname, caller, caller_id, plugins = None, meta = False):
        self.pathname   = pathname
        self.dir        = os.path.isdir(pathname)
        self.mask       = 0
        self.maskname   = 'SB_IN_SCAN'
        self.caller     = caller
        self.caller_id  = caller_id
        self.plugins    = plugins
        self.meta       = meta
        self.state      = {}
        self.plugs_flag = threading.Event()


class SosBackupsScanCompleteEvent(SosBackupsScanEvent):
    def __init__(self, pathname, caller, caller_id, plugins = None, meta = True):
        SosBackupsScanEvent.__init__(self, pathname, caller, caller_id, plugins, meta)


class SosBackupsCronScan(object):
    def __init__(self, name, paths, options = {}, notifiers = None):
        self.caller            = 'cronsync'
        self.caller_id         = "%s" % uuid.uuid4()
        self.current_time      = datetime.datetime.now()
        self.current_utc_time  = datetime.datetime.utcnow()
        self.name              = name
        self.paths             = paths
        self.inotify           = DWHO_SHARED.get('sosbackups', 'inotify')
        self.options           = options or {}
        self.options['format'] = self.options.get('format') or False
        self.notifications     = bool(self.options.get('notifications')) or False
        self.exclude_patterns  = set()
        self.include_plugins   = []
        self.plugins           = {}

        self.path              = None
        self.errors            = []
        self.started_at        = None
        self.ended_at          = None
        self.duration          = -1
        self.stats             = {}

        self.events            = []
        self.notifiers         = notifiers

        self.workerpool        = workerpool.WorkerPool(max_workers = int(self.options.get('max_workers') or 1),
                                                       life_time   = self.options.get('worker_lifetime', WORKER_LIFETIME),
                                                       name        = 'cronscan')
        self.handler           = DWhoInotifyEventHandler(dw_inotify = self.inotify,
                                                         workerpool = self.workerpool)

        if 'plugins' in self.options:
            plugins = self.options.pop('plugins')
            if isinstance(plugins, basestring):
                self.include_plugins = [plugins]
            elif isinstance(plugins, list):
                self.include_plugins = plugins
            elif isinstance(plugins, dict):
                for plug_name, plug_opts in plugins.iteritems():
                    if not plug_opts:
                        continue
                    self.include_plugins.append(plug_name)

                    if isinstance(plug_opts, dict):
                        self.plugins[plug_name] = plug_opts

        if 'exclude_files' in self.options:
            exclude_files = self.options.pop('exclude_files')

            if isinstance(exclude_files, basestring):
                exclude_files = [exclude_files]
            elif not isinstance(exclude_files, list):
                LOG.error("invalid exclude_files type. (exclude_files: %r)",
                          exclude_files)
                exclude_files = []

            for x in exclude_files:
                pattern = helpers.load_patterns_from_file(x)
                if not pattern:
                    raise DWhoConfigurationError("unable to load exclude patterns from %r." % x)

                self.exclude_patterns.update(pattern)

        if self.exclude_patterns:
            self.exclude_patterns = pyinotify.ExcludeFilter(list(self.exclude_patterns))
        else:
            self.exclude_patterns = None

    def _parse_time_opt(self, value, utc = False):
        if value == 'start':
            if utc:
                return self.current_utc_time
            else:
                return self.current_time
        elif isinstance(value, dict) and 'when' in value:
            xtime = self._parse_time_opt(value['when'], utc)

            if isinstance(xtime, datetime.datetime):
                if 'args' in value:
                    return datetime.timedelta(*value['args']) + xtime
                elif 'kwargs' in value:
                    return datetime.timedelta(**value['kwargs']) + xtime

            return xtime

    def _get_state(self, status):
        return {'caller':     self.caller,
                'caller_id':  self.caller_id,
                'status':     status,
                'started_at': self.started_at,
                'ended_at':   self.ended_at,
                'errors':     self.errors,
                'duration':   self.duration,
                'path':       self.path,
                'stats':      self.stats}

    def _add_stats(self, key, stats):
        for xtype, values in self.stats[key].iteritems():
            if xtype not in stats:
                continue
            for x in values.iterkeys():
                if x in stats[xtype]:
                    self.stats[key][xtype][x] += stats[xtype][x]

    def clean_events(self, wait = False):
        to_remove = []
        for event in self.events:
            if _KILLED:
                return

            if wait is not False:
                event.plugs_flag.wait(wait)
            if not event.plugs_flag.is_set():
                continue
            for plugin, state in event.state.iteritems():
                if state.get('errors'):
                    self.errors.extend(state['errors'])
                if state.get('stats'):
                    if plugin not in self.stats:
                        self.stats[plugin] = copy.deepcopy(DEFAULT_STATS)
                    self._add_stats(plugin, state['stats'])
                    self._add_stats('__total', state['stats'])

            to_remove.append(event)

        for x in to_remove:
            self.events.remove(x)

        del to_remove

    def run(self, xpath):
        options     = self.options.copy()
        plugins     = self.plugins.copy()

        file_type   = options.get('file_type')
        followlinks = bool(options.get('follow'))
        is_root     = True

        filepath    = None
        cfg_path    = None

        xvars   = {}
        if 'vars' in options:
            xvars = options.pop('vars') or {}

        if options['format']:
            fkwargs = {'env': os.environ,
                       'gmtime': datetime.datetime.utcnow(),
                       'time': datetime.datetime.now(),
                       'vars': xvars}
            xpath = xpath.format(**fkwargs)

        if not os.path.exists(xpath):
            LOG.error("path doesn't exist: %r", xpath)
            return

        for plug_opts in plugins.itervalues():
            if '__time__' in plug_opts:
                plug_opts['__time__'] = self._parse_time_opt(plug_opts['__time__'])

            if '__gmtime__' in plug_opts:
                plug_opts['__gmtime__'] = self._parse_time_opt(plug_opts['__gmtime__'], True)

        for root, dirs, files in os.walk(xpath, topdown = True, followlinks = followlinks):
            if _KILLED:
                return

            if self.exclude_patterns and self.exclude_patterns(root):
                is_root = False
                dirs[:] = []
                LOG.debug("exclude path from scan. (path: %r)", root)
                continue

            if file_type == 'directory':
                if not is_root:
                    xfiles  = dirs
                else:
                    is_root = False
                    xfiles  = files
            else:
                xfiles    = files
                file_type = 'file'

            (last_filepath, last_cfg_path) = (None, None)

            for filename in xfiles:
                if _KILLED:
                    return

                filepath = os.path.join(root, filename)

                if self.exclude_patterns and self.exclude_patterns(filepath):
                    LOG.debug("exclude %s from scan. (filepath: %r)", file_type, filepath)
                    continue

                cfg_path = self.inotify.get_cfg_path(filepath)
                if not cfg_path:
                    continue

                event    = SosBackupsScanEvent(filepath,
                                               self.caller,
                                               self.caller_id,
                                               plugins)

                self.handler.call_plugins(cfg_path,
                                          event,
                                          include_plugins = self.include_plugins,
                                          exclude_filter  = False)

                self.clean_events(wait = False)
                self.events.append(event)

        return (filepath, cfg_path, plugins)

    def _pre_run(self, xpath):
        self.started_at = time.strftime(DATE_FORMAT)
        self.ended_at   = None
        self.path       = xpath
        self.errors     = []
        self.duration   = -1
        self.events     = []
        self.stats      = {'__total': copy.deepcopy(DEFAULT_STATS)}

        if self.notifications:
            self.notifiers(self._get_state('processing'))

    def _complete_event(self, filepath, cfg_path, plugins = None):
        if not filepath or not cfg_path:
            return

        event = SosBackupsScanCompleteEvent(filepath,
                                            self.caller,
                                            self.caller_id,
                                            plugins)
        self.handler.call_plugins(cfg_path,
                                  event,
                                  include_plugins = self.include_plugins,
                                  exclude_filter  = False)
        LOG.debug("starting complete scan event. (path: %r)", self.path)
        event.plugs_flag.wait()
        LOG.debug("stopping complete scan event. (path: %r)", self.path)

    def _post_run(self):
        LOG.debug("starting clean events. (path: %r)", self.path)
        self.clean_events(wait = None)
        LOG.debug("stopping clean events. (path: %r)", self.path)

        self.ended_at = time.strftime(DATE_FORMAT)
        started       = datetime.datetime.strptime(self.started_at, DATE_FORMAT)
        self.duration = (datetime.datetime.now() - started).total_seconds()

        if not self.errors:
            state = self._get_state('success')
        else:
            state = self._get_state('failure')

        if self.notifications:
            self.notifiers(state)

    def __call__(self):
        self.inotify.scan_event.wait()

        for xpath in self.paths:
            self._pre_run(xpath)

            filepath, cfg_path, plugins = (None, None, None)

            try:
                (filepath, cfg_path, plugins) = self.run(xpath)
            except Exception, e:
                self.errors.append({'error': traceback.format_exc(),
                                    'filepath': xpath,
                                    'logged_at': time.strftime(DATE_FORMAT),
                                    'stderr': None})
                LOG.exception(e)

            self._complete_event(filepath, cfg_path, plugins)
            self._post_run()

        if self.workerpool:
            self.workerpool.killall(1)

        del self.events

        return self.name


class SosBackupsCronSyncThread(threading.Thread):
    def __init__(self, cron_pool, tabs, notifiers):
        threading.Thread.__init__(self)
        self.cron_pool = cron_pool
        self.tabs      = tabs
        self.notifiers = notifiers
        self.runners   = []
        self.history   = {}

    def callback(self, name):
        if name in self.runners:
            self.runners.remove(name)

    def run(self):
        while not _KILLED:
            for tab, tasks in self.tabs.iteritems():
                if not isinstance(tasks, list):
                    LOG.error("invalid tasks type, must be a list: %r", tasks)

                for params in tasks:
                    options = params.copy()
                    if isinstance(options['paths'], list):
                        paths = list(options.pop('paths'))
                    else:
                        paths = [options.pop('paths')]

                    name    = "%s:%s" % (tab, hashlib.sha1(':'.join(paths)).hexdigest())

                    if name not in self.history:
                        self.history[name] = []

                    if name in self.runners:
                        continue

                    t = datetime.datetime.now().strftime(_CRON_DATE_FORMAT)

                    if t in self.history[name]:
                        if len(self.history[name]) > 120:
                            del self.history[name][0:120]
                        continue

                    self.history[name].append(t)

                    i = croniter(tab, datetime.datetime.now())
                    p = i.get_prev(datetime.datetime).strftime(_CRON_DATE_FORMAT)
                    n = i.get_next(datetime.datetime).strftime(_CRON_DATE_FORMAT)

                    if t in (p, n):
                        self.runners.append(name)
                        self.cron_pool.run(SosBackupsCronScan(name, paths, options, self.notifiers), self.callback)

            time.sleep(1)


class SosBackupsCronSyncPlugin(DWhoPluginBase):
    PLUGIN_NAME = 'cronsync'

    def safe_init(self):
        tabs      = self.plugconf['tabs']
        notifiers = None

        if self.config['general'].get('notifiers_path'):
            notifiers = DWhoPushNotifications(self.server_id,
                                              self.config['general']['notifiers_path'])

        self.cron_pool = workerpool.WorkerPool(max_workers = int(self.plugconf.get('max_workers') or len(tabs)),
                                               life_time   = self.plugconf.get('worker_lifetime', WORKER_LIFETIME),
                                               name        = 'cronsync')
        self.cron_sync = SosBackupsCronSyncThread(self.cron_pool, tabs, notifiers)
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
        PLUGINS.register(SosBackupsCronSyncPlugin())
    _start()
