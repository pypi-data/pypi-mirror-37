# sgejob

## 1 Introduction
To collect SGE job information with a damemon. see https://github.com/linzhi2013/sgejob

## 2 Installation

Make sure your `pip` is from Python3

    $ pip install sgejob

There will be a command `sgejob_daemon` created under the same directory where your `pip` command located.


If you want to learn more about Python3 and `pip`, please refer to `https://www.python.org/` and `https://docs.python.org/3/tutorial/venv.html?highlight=pip`.

## 3 Usage
	
	$ sgejob_daemon

        usage: sgejob_daemon.py [-h] [-qstat <str>] [-user <str>] [-PIDFILE <file>]
                                [-DAEMON_LOG <file>] [-sge_infor_file <file>]
                                [-sge_usage_file <file>] [-interval INTERVAL]
                                {start,stop} ...

        Start and stop a daemon to collect SGE job information. see https://github.com/linzhi2013/sgejob

        Copyright (c) 2018 Guanliang Meng (see https://github.com/linzhi2013).

        The function `daemonize()` part was copied from
        `https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p14_launching_daemon_process_on_unix.html`,
        which is licensed under the Apache License, Version 2.0.



        positional arguments:
          {start,stop}
            start               start the daemon
            stop                stop the daemon

        optional arguments:
          -h, --help            show this help message and exit
          -qstat <str>          the qstat command to be used [qstatt]
          -user <str>           whose SGE jobs to be collected? [mengguanliang]
          -PIDFILE <file>       set PIDFILE path [/home/mengguanliang/sge_daemon.pid]
          -DAEMON_LOG <file>    set DAEMON_LOG path
                                [/home/mengguanliang/sge_daemon.log]
          -sge_infor_file <file>
                                set sge infor_file path
                                [/home/mengguanliang/sge.infor_df.csv]
          -sge_usage_file <file>
                                set sge usage_file path
                                [/home/mengguanliang/sge.usage_df.csv]
          -interval INTERVAL    how often to check the SGE job status? [300]

### using as a module


      In [5]: from sgejob import UserJobs, SgeJob, record_jobs

      In [6]: UserJobs?
      Init signature: UserJobs(user=None, qstat='qstat')
      Docstring:
      `UserJobs` object has one attribute `jobs`, which is a dictionary, whose keys are the sge job numbers.

      Then `UserJobs.jobs[job_number]` is also a dictionary, whic has following
      keys:

      ['JB_job_number', 'JAT_prio', 'JB_name', 'JB_owner', 'state',
       'JAT_start_time', 'queue_name', 'slots']
      File:           ~/soft/script/sgejob/source/v0.0.1/sgejob/sgejob.py
      Type:           type

      In [7]: SgeJob?
      Init signature: SgeJob(job_number=None, qstat='qstat')
      Docstring:
      `SgeJob` object has two attributes: `infor` and `usage`.

      `SgeJob.infor` is a dictionary, corresponding to the output content of
      `qstat -j job_number`, where the first column is the key, the second column
      is the value.

      `SgeJob.usage` is also a dictionary, whose content is from
      `SgeJob.infor['usage         1']`.


      `SgeJob.infor` has following keys:

      ['current_time', 'job_number', 'exec_file', 'submission_time', 'owner',
       'uid', 'group', 'gid', 'sge_o_home', 'sge_o_log_name', 'sge_o_path',
       'sge_o_shell', 'sge_o_workdir', 'sge_o_host', 'account', 'cwd',
       'hard resource_list', 'mail_list', 'notify', 'job_name', 'jobshare',
       'hard_queue_list', 'env_list', 'script_file', 'project', 'binding',
       'job_type', 'usage         1', 'binding       1', 'scheduling info']


      `SgeJob.usage` has following keys:

      ['current_time', 'job_number', 'cpu', 'mem', 'io', 'vmem', 'maxvmem']
      File:           ~/soft/script/sgejob/source/v0.0.1/sgejob/sgejob.py
      Type:           type

      In [8]: record_jobs?
      Signature: record_jobs(user=None, qstat='qstat', running_only=True, infor_df_csvfile=None, usage_df_csvfile=None)
      Docstring:
      Collect job information and append to infor_df_csvfile and
      usage_df_csvfile.

      user=None, collect current user's jobs.

      if running_only=True, it will only collect the running jobs.

      return: None.
      File:      ~/soft/script/sgejob/source/v0.0.1/sgejob/sgejob.py
      Type:      function


## 5 Citations
Currently, I have no plan to publish `sgejob`.

## 6 Author

Guanliang MENG.



