#!/usr/bin/env python3
# daemon.py
# copied from https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p14_launching_daemon_process_on_unix.html

import os
import sys

import atexit
import signal

import argparse
import getpass

def get_para():
    desc = '''
Start and stop a daemon to collect SGE job information.

Copyright (c) 2018 Guanliang Meng (see https://github.com/linzhi2013/sgejob).

The function `daemonize()` part was copied from
`https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p14_launching_daemon_process_on_unix.html`,
which is licensed under the Apache License, Version 2.0.

    '''

    HOMEDIR = os.getenv('HOME')
    HOMEDIR = os.path.join(HOMEDIR, 'sge_daemon_records')
    if not os.path.exists(HOMEDIR):
        os.chdir(HOMEDIR)

    parser = argparse.ArgumentParser(prog="sgejob_daemon.py",
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')

    start_parser = subparsers.add_parser('start',
        help="start the daemon")

    stop_parser = subparsers.add_parser('stop',
        help='stop the daemon')


    parser.add_argument('-qstat', metavar='<str>', default='qstat',
        help='the qstat command to be used [%(default)s]')

    parser.add_argument('-user', metavar='<str>',
        default=getpass.getuser(),
        help='whose SGE jobs to be collected? [%(default)s]')

    parser.add_argument('-running_only', action='store_false', default=True,
        help='only qstat to the jobs which are running [%(default)s]')

    parser.add_argument('-PIDFILE', metavar='<file>',
        default=os.path.join(HOMEDIR, 'sge_daemon.pid'),
        help=argparse.SUPPRESS)

    parser.add_argument('-DAEMON_LOG', metavar='<file>',
        default=os.path.join(HOMEDIR, 'sge_daemon.log'),
        help=argparse.SUPPRESS)

    parser.add_argument('-sge_infor_file', metavar='<file>',
        default=os.path.join(HOMEDIR, 'sge.infor_df.csv'),
        help='set sge infor_file path [%(default)s]')

    parser.add_argument('-sge_usage_file', metavar='<file>',
        default=os.path.join(HOMEDIR, 'sge.usage_df.csv'),
        help='set sge usage_file path [%(default)s]')


    parser.add_argument('-interval', type=int, default=300,
        help='how often to check the SGE job status? [%(default)s]')

    parser.add_argument('-JB_name_expr', metavar='<str>',
        help='only check the jobs whose names match the regular expression')



    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def daemonize(pidfile, *, stdin='/dev/null',
                          stdout='/dev/null',
                          stderr='/dev/null'):

    if os.path.exists(pidfile):
        raise RuntimeError('Already running')

    # First fork (detaches from parent)
    try:
        if os.fork() > 0:
            raise SystemExit(0)   # Parent exit
    except OSError as e:
        raise RuntimeError('fork #1 failed.')

    os.chdir('/')
    os.umask(0)
    os.setsid()
    # Second fork (relinquish session leadership)
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 failed.')

    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # Replace file descriptors for stdin, stdout, and stderr
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    # Write the PID file
    with open(pidfile,'w') as f:
        print(os.getpid(),file=f)

    # Arrange to have the PID file removed on exit/signal
    atexit.register(lambda: os.remove(pidfile))
    # atexit.register() 函数注册了一个函数在Python解释器终止时执行。

    # Signal handler for termination (required)
    def sigterm_handler(signo, frame):
        raise SystemExit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)


def job_recording(qstat=None, user=None, JB_name_expr=None, running_only=True, sge_infor_file=None, sge_usage_file=None, interval=300):
    # 需要执行的主体任务
    from sgejob import record_jobs
    import time

    while True:
        record_jobs(qstat=qstat,
                    user=user,
                    JB_name_expr=JB_name_expr,
                    running_only=running_only,
                    infor_df_csvfile=sge_infor_file,
                    usage_df_csvfile=sge_usage_file)

        time.sleep(interval)


def main():
    args = get_para()

    qstat = args.qstat
    user = args.user
    running_only = args.running_only
    PIDFILE = args.PIDFILE
    DAEMON_LOG = args.DAEMON_LOG
    sge_infor_file = args.sge_infor_file
    sge_usage_file = args.sge_usage_file
    interval = args.interval
    JB_name_expr = args.JB_name_expr

    command = args.command

    if command == 'start':
        try:
            daemonize(PIDFILE,
                      stdout=DAEMON_LOG,
                      stderr=DAEMON_LOG)
        except RuntimeError as e:
            print(e, file=sys.stderr)
            raise SystemExit(1)

        # 到现在，守护进程已经成功创建。
        # 接着，在守护进程中运行main()函数
        job_recording(qstat=qstat,
                    user=user,
                    JB_name_expr=JB_name_expr,
                    running_only=running_only,
                    sge_infor_file=sge_infor_file,
                    sge_usage_file=sge_usage_file,
                    interval=interval)

    elif command == 'stop':
        if os.path.exists(PIDFILE):
            with open(PIDFILE) as f:
                # Send signal sig to the process pid.
                # Constants for the specific signals available on the host
                # platform are defined in the signal module.
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print('Not running', file=sys.stderr)
            raise SystemExit(1)

    else:
        print('Unknown command {!r}'.format(command), file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()