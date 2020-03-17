#!/bin/bash

here=`dirname $0`
src=$here/../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports

tgt=$here/data/cases.csv
wrk=$tgt.wrk
hdrs=$src/03-16-2020.csv

tgtdir=`dirname $tgt`

if [ ! -d tgtdir ]; then
  mkdir -p $tgtdir
fi

head -n1 $hdrs > $wrk

for f in $src/*.csv; do
  echo adding $f to $wrk
  tail -n+2 $f >> $wrk
  echo >> $wrk
done

sed '/^$/d' $wrk > $tgt

