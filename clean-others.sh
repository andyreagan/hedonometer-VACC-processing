#PBS -l nodes=1:ppn=1
#PBS -l walltime=02:00:00
#PBS -N realtimeScrape
#PBS -j oe

cd /users/a/r/areagan/scratch/realtime-parsing

for YEAR in 2008 2009 2010 2011 2012 2013 2014 2015
do
  for DICT in Liu LIWC ANEW Warriner MPQA
  do
    echo "cleaning ${DICT} in ${YEAR}"
    # zip ${DICT}.zip word-vectors/${YEAR}*/*-${DICT}.csv
    \rm word-vectors/${YEAR}*/*-${DICT}.csv
  done
done
