#!/bin/bash

INPUTDIR=$1
JOBS=`mktemp`
WD=`pwd`
cd $INPUTDIR
ls wkday*.match > $JOBS
cd $WD

LOG=/tmp/target.log

trap "echo 'User interrupt.'; rm $JOBS; exit" INT

for W in `cat $JOBS`
do
	echo `date` "-- Processing $W"
	./solver.py $INPUTDIR/$W $W.csv >> $LOG 2>&1
done

rm $JOBS
