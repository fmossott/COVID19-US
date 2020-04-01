#!/bin/sh

cd `dirname $0`
python3 pyscript/mergeTimeSeries.py -s ../COVID-19/csse_covid_19_data/csse_covid_19_time_series/ -o data/ts_raw.csv
python3 pyscript/mergeDailyReports.py -s ../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/ -o data/
python3 pyscript/mergeWorldData.py -s ../COVID-19/csse_covid_19_data/csse_covid_19_time_series/
python3 pyscript/mergeUSStatesData.py -s ../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/