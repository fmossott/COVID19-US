#!/bin/bash

here=`dirname $0`
src=$here/../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports

tgt=$here/data/cases.csv

tgtdir=`dirname $tgt`

if [ ! -d tgtdir ]; then
  mkdir -p $tgtdir
fi

first=true
for f in $src/*.csv; do
  echo adding $f to $tgt
  if $first ; then
    head -n1 $f > $tgt
    first=false
  fi
  tail -n+2 $f >> $tgt
done

