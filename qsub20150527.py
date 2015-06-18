# accept a timestamp
# read the current date
# pump out a qsub script named by the timestamp, for the current date

import datetime
import sys
import subprocess
import time
from os.path import isdir,isfile
from os import mkdir

if True:
    ctime = "tmp"
    
    # get the current time, and give 0 hours
    # for submitted jobs to work through
    now = datetime.datetime(2015,5,27,23,59)
    # floor the last 15 minutes
    now -= datetime.timedelta(minutes=now.minute % 15,
                              seconds=now.second,
                              microseconds=now.microsecond)
    # get yesterday
    yesterday = now-datetime.timedelta(days=1)
    fifteen_minutes = datetime.timedelta(minutes=15)
    
    # loop through the 15 minutes until yesterday
    # and make all of the files that are missing
    date = now
    while date > yesterday:
        print(date)
        if not isdir(date.strftime('word-vectors/%Y-%m-%d-nofilter')):
            mkdir(date.strftime('word-vectors/%Y-%m-%d-nofilter'))
            mkdir(date.strftime('word-dicts/%Y-%m-%d-nofilter'))
        script = '''export DATE={0}
export HOUR={1}
export MINUTE={2}
qsub -qshortq -V run-nofilter.qsub
\\rm {3}.sh

'''.format(date.strftime('%Y-%m-%d'),date.strftime('%H'),date.strftime('%M'),ctime)
        print('writing {}.sh'.format(ctime))
        f = open('{}.sh'.format(ctime),'w')
        f.write(script)
        f.close()
    
        qstatus = subprocess.check_output(". {}.sh".format(ctime),shell=True)
        print(qstatus)
        time.sleep(.1)
        date -= fifteen_minutes
    









