#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:30:00
#PBS -N realtimeScrape
#PBS -j oe

cd /users/a/r/areagan/scratch/realtime-parsing
# . RHEL7-python-3.5.1/bin/activate

export DATE=$(date --date="yesterday" +"%Y-%m-%d")
for HOUR in 0{0..9} {10..23}
do
export HOUR
/opt/pbs/bin/qsub -qshortq -V run-hour-RHEL7-python3.5.1.qsub
# for MINUTE in 00 15 30 45
# do
#   export MINUTE
#   echo "processing ${DATE}-${HOUR}-${MINUTE}"
#   # /usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/${DATE}/${DATE}-${HOUR}-${MINUTE}.gz | /gpfs1/arch/x86_64-rhel7/python-3.5.1/bin/python3.5 realtime.py "${DATE}" "${DATE}-${HOUR}-${MINUTE}"
#   # /usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/${DATE}/${DATE}-${HOUR}-${MINUTE}.gz | python realtime-py3.py "${DATE}" "${DATE}-${HOUR}-${MINUTE}"
# done
done
