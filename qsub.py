# accept a timestamp
# read the current date
# pump out a qsub script named by the timestamp, for the current date

import datetime
import sys
import subprocess
import time
from os.path import isdir,isfile
from os import mkdir

max_jobs = 100

jobs = int(subprocess.check_output("showq | grep areagan | wc -l",shell=True))
print("there are {0} jobs via showq".format(jobs))

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
    yesterday = datetime.datetime.now()-datetime.timedelta(days=100)
    fifteen_minutes = datetime.timedelta(minutes=15)
    
    # loop through the 15 minutes until yesterday
    # and make all of the files that are missing
    date = now
    while date > yesterday and jobs_remaining > 0:
        if not isdir(date.strftime('word-vectors/%Y-%m-%d')):
            mkdir(date.strftime('word-vectors/%Y-%m-%d'))
            mkdir(date.strftime('word-dicts/%Y-%m-%d'))
        if isfile(date.strftime('/users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/%Y-%m-%d/%Y-%m-%d-%H-%M.gz')) and not isfile(date.strftime('/users/a/r/areagan/fun/twitter/realtime-parsing/word-vectors/%Y-%m-%d/%Y-%m-%d-%H-%M.csv')):
            jobs_remaining -= 1

            script = '''export DATE={0}
export HOUR={1}
export MINUTE={2}
qsub -qshortq -V run.qsub
\\rm {3}.sh

'''.format(date.strftime('%Y-%m-%d'),date.strftime('%H'),date.strftime('%M'),ctime)

            print('writing {}.sh'.format(ctime))
            f = open('{}.sh'.format(ctime),'w')
            f.write(script)
            f.close()
    
            qstatus = subprocess.check_output(". {}.sh".format(ctime),shell=True)
            print(qstatus)
            time.sleep(.25)
        date -= fifteen_minutes










