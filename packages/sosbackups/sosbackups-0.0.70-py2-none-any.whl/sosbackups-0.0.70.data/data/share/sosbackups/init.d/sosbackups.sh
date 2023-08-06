#!/bin/sh

PATH=/opt/bin:/opt/sbin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/syno/sbin:/usr/syno/bin:/usr/local/sbin:/usr/local/bin

sysctl -w fs.inotify.max_queued_events=131072 >/dev/null
sysctl -w fs.inotify.max_user_instances=131072 >/dev/null
sysctl -w fs.inotify.max_user_watches=1048576 >/dev/null

. /etc.defaults/rc.subr                 # for LSB definition and utilities

RM="rm"
MKDIR="mkdir"
DIRNAME="dirname"
IONICE="$(which ionice)"
NICE="$(which nice)"
ProcName="sosbackups"
SosBackups="$(which $ProcName)"
SosBackupsConfFile="/etc/sosbackups/sosbackups.yml"
SosBackupsPidFile="/var/run/$ProcName.pid"
SosBackupsLogFile="/var/log/sosbackups/daemon.log"

OPTS="-c $SosBackupsConfFile --logfile $SosBackupsLogFile"

if [ -f "/etc/sosbackups/rc.default" ];
then
    . /etc/sosbackups/rc.default
fi

EXTRA_OPTS="${EXTRA_OPTS:-"-l info"}"

StartSosBackupsDaemon()
{
    $MKDIR `$DIRNAME "$SosBackupsPidFile"` 2>/dev/null || true
    $MKDIR `$DIRNAME "$SosBackupsLogFile"` 2>/dev/null || true
    if [ -x "$SosBackups" ]; then
        CMD="$SosBackups -p $SosBackupsPidFile ${OPTS} ${EXTRA_OPTS}"
        if [ ! -z "${NICE}" ];
        then
            CMD="${NICE} -n 19 ${CMD}"
        fi

        if [ ! -z "${IONICE}" ];
        then
            CMD="${IONICE} -c 3 ${CMD}"
        fi

        ${CMD}
    else
        echo "$SosBackups is not executable."
    fi
}

StopSosBackupsDaemon()
{
    if [ -f "$SosBackupsPidFile" ]; then
        PROCESS_PID=`cat $SosBackupsPidFile`
        kill -9 $PROCESS_PID
        $RM $SosBackupsPidFile
    fi
}

case "$1" in
stop)
    StopSosBackupsDaemon
    ;;
start)
    StartSosBackupsDaemon
    ;;
restart)
    $0 stop
    sleep 1
    $0 start
    ;;
status)
	if pidof sosbackups ; then
		if [ -f $SosBackupsPidFile ] ; then
			pid=`cat $SosBackupsPidFile`
			if [ 0 != `ps x | grep $ProcName | grep $pid | wc -l` ]; then
				exit $LSB_STAT_RUNNING
			else
				exit $LSB_STAT_DEAD_FPID
			fi
		fi
		exit $LSB_STAT_RUNNING
	else
		if [ -f $SosBackupsPidFile ] ; then
			exit $LSB_STAT_DEAD_FPID
		else
			exit $LSB_STAT_NOT_RUNNING
		fi
	fi &>/dev/null
    ;;
*)
    echo "usage: $0 { start | stop | restart | status }" >&2
    exit 1
    ;;
esac
