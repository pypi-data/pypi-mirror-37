#!/usr/bin/env python3
import subprocess
import pandas as pd
import re
import getpass
import xml.etree.ElementTree as ET
import time


class JobDoesNotExist(Exception):
    """docstring for JobDoesNotExists"""
    def __init__(self, arg):
        super(JobDoesNotExist, self).__init__()
        self.arg = arg

    def __str__(self):
        return repr(self.arg)


class UsageNotFound(Exception):
    """docstring for UsageNotFound"""
    def __init__(self, arg):
        super(UsageNotFound, self).__init__()
        self.arg = arg

    def __str__(self):
        return repr(self.arg)


class SgeJob(object):
    """
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

    """

    def __init__(self, job_number=None, qstat='qstat'):
        super(SgeJob, self).__init__()
        self.infor = self.get_job_infor(job_number=job_number, qstat=qstat)

        usage_k = ''
        for k in self.infor:
            m = re.search(r'^(usage\s+1)$', k)
            if m:
                usage_k = k
                break

        if not usage_k:
            raise UsageNotFound('Not found usage for {0}'.format(job_number))

        self.usage = self.get_usage(self.infor[usage_k])
        self.usage['job_number'] = self.infor['job_number']
        self.usage['current_time'] = self.infor['current_time']


    def get_job_infor(self, job_number, qstat='qstat'):
        cmd = '{qstat} -j {job_number}'.format(
            qstat=qstat, job_number=job_number)

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = subprocess.check_output(
            cmd, shell=True, universal_newlines=True)

        if not content:
            raise JobDoesNotExist('{job_number} no longer exists!'.format(job_number=job_number))

        infor = {}
        infor['current_time'] = current_time
        for line in content.splitlines():
            if line.startswith('===='):
                continue
            try:
                key, val = re.split(r':\s+', line, maxsplit=1)
            except ValueError:
                continue

            infor[key] = val

        return infor


    def get_usage(self, usage_val):
        usage = {}
        for i in re.split(r',\s+', usage_val):
            key, val = re.split(r'\=', i, maxsplit=1)
            usage[key] = val

        return usage


class UserJobs(object):
    """
    `UserJobs` object has one attribute `jobs`, which is a dictionary, whose keys are the sge job numbers.

    Then `UserJobs.jobs[job_number]` is also a dictionary, whic has following
    keys:

    ['JB_job_number', 'JAT_prio', 'JB_name', 'JB_owner', 'state',
     'JAT_start_time', 'queue_name', 'slots']

    """

    def __init__(self, user=None, qstat='qstat'):
        super(UserJobs, self).__init__()
        if not user:
            user = getpass.getuser()
        self.jobs = self.get_jobs(user=user, qstat=qstat)


    def xml2dict(self, xml_data):
        root = ET.XML(xml_data)  # element tree
        all_records = []
        for child in root:
            for subchild in child:
                record = {}
                for subsubchild in subchild:
                    record[subsubchild.tag] = subsubchild.text
                all_records.append(record)

        record_dict = {}
        for record in all_records:
            job_number = record['JB_job_number']
            record_dict[job_number] = record

        return record_dict


    def get_jobs(self, user, qstat='qstat'):
        if not user:
            user = getpass.getuser()

        cmd = '{qstat} -xml -u {user}'.format(qstat=qstat, user=user)

        jobs_xml = subprocess.check_output(
            cmd, shell=True, universal_newlines=True)

        return self.xml2dict(jobs_xml)


    def __len__(self):
        return len(self.jobs)


def record_jobs(user=None, qstat='qstat', JB_name_expr=None, running_only=True, infor_df_csvfile=None, usage_df_csvfile=None):
    '''
    Collect job information and append to infor_df_csvfile and
    usage_df_csvfile.

    user=None, collect current user's jobs.

    if running_only=True, it will only collect the running jobs.

    return: None.

    '''

    if not user:
        user = getpass.getuser()
    userjobs = UserJobs(user=user, qstat=qstat)

    if len(userjobs) == 0:
        # if there are no jobs
        return None

    for job_number in userjobs.jobs:
        if JB_name_expr and (not re.search(JB_name_expr, userjobs.jobs[job_number]['JB_name'])):
            continue

        if running_only and userjobs.jobs[job_number]['state'] == 'r':
            try:
                sgejob = SgeJob(job_number=job_number, qstat=qstat)
            except JobDoesNotExist:
                continue
            except UsageNotFound:
                continue
        else:
            try:
                sgejob = SgeJob(job_number=job_number, qstat=qstat)
            except JobDoesNotExist:
                continue
            except UsageNotFound:
                continue

        with open(infor_df_csvfile, 'a') as fhout:
            infor_df = pd.DataFrame([sgejob.infor])
            infor_df.to_csv(fhout, header=fhout.tell()==0, index=False)

        with open(usage_df_csvfile, 'a') as fhout:
            usage_df = pd.DataFrame([sgejob.usage])
            usage_df.to_csv(fhout, header=fhout.tell()==0, index=False)

    return None

