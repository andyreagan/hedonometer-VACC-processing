# accept a timestamp
# read the current date
# pump out a qsub script named by the timestamp, for the current date

import datetime
import sys
import subprocess
import time
from os.path import isdir,isfile
from os import mkdir,chmod

max_jobs = 200

jobs = int(subprocess.check_output("showq | grep areagan | wc -l",shell=True))
print("there are {0} jobs via showq".format(jobs))

print(subprocess.check_output("pwd",shell=True))

if jobs < max_jobs:
    # ctime = subprocess.check_output("date +%S.%M.%H.%d.%m.%y",shell=True).rstrip()
    # job submission is synchronous.... so don't worry about writing out different files
    # the only reason to write out the shell script in the first place is to make sure that env variables make it to the job
    ctime = "tmp"
    
    jobs_remaining = max_jobs-jobs

    # get the current time, and give 0 hours
    # for submitted jobs to work through
    now = datetime.datetime.now() # -datetime.timedelta(hours=2)
    # floor the last 15 minutes
    now -= datetime.timedelta(minutes=now.minute % 15,
                              seconds=now.second,
                              microseconds=now.microsecond)
    # get yesterday
    yesterday = now-datetime.timedelta(days=40)
    # yesterday = datetime.datetime(2008,9,9)
    # delta = datetime.timedelta(minutes=15)
    delta = datetime.timedelta(hours=1)
    
    # loop through the 15 minutes until yesterday
    # and make all of the files that are missing
    date = now
    while date > yesterday and jobs_remaining > 0:
        if not isdir(date.strftime('word-vectors/%Y-%m-%d')):
            mkdir(date.strftime('word-vectors/%Y-%m-%d'))
            mkdir(date.strftime('word-dicts/%Y-%m-%d'))
        if isfile(date.strftime('/users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/%Y-%m-%d/%Y-%m-%d-%H-45.gz')) and not isfile(date.strftime('/users/a/r/areagan/scratch/realtime-parsing/word-vectors/%Y-%m-%d/%Y-%m-%d-%H-45.csv')):
        # if not isfile(date.strftime('/users/a/r/areagan/scratch/realtime-parsing/word-vectors/%Y-%m-%d/%Y-%m-%d-%H-%M.csv')):
            jobs_remaining -= 1

            script = '''export DATE={0}
export HOUR={1}
# export MINUTE={2}
# qsub -qshortq -V run-hour.qsub
# qsub -V run-hour.qsub
qsub -qshortq -V run-hour-RHEL7-python3.5.1.qsub
# \\rm {3}.sh
'''.format(date.strftime('%Y-%m-%d'),date.strftime('%H'),date.strftime('%M'),ctime)

            print(date.strftime('word-vectors/%Y-%m-%d/%Y-%m-%d-%H-%M.csv'))
            
            # print('writing {}.sh'.format(ctime))
            f = open('/users/a/r/areagan/scratch/realtime-parsing/{}.sh'.format(ctime),'w')
            f.write(script)
            f.close()
            # chmod('/users/a/r/areagan/scratch/realtime-parsing/{}.sh'.format(ctime),0o777)
            # no need to touch when running every hour (jobs are much faster)
            # but this is needed when running retroactively so no overlap
            # a = subprocess.check_output("touch {0}".format(date.strftime('/users/a/r/areagan/scratch/realtime-parsing/word-vectors/%Y-%m-%d/%Y-%m-%d-%H-%M.csv')),shell=True)
            
            # qstatus = subprocess.check_output("which qsub".format(ctime),shell=True,stderr=subprocess.STDOUT)
            # print(qstatus)
            # qstatus = subprocess.check_output("/users/a/r/areagan/scratch/realtime-parsing/dir.sh".format(ctime),shell=True,stderr=subprocess.STDOUT)
            # print(qstatus)
            qstatus = subprocess.check_output("/users/a/r/areagan/scratch/realtime-parsing/{}.sh".format(ctime),shell=True,stderr=subprocess.STDOUT)
            print(qstatus)
            time.sleep(.25)
        date -= delta










