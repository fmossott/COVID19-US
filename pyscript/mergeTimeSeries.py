# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import glob
import argparse

# %%
parser = argparse.ArgumentParser(description='Merge time series values')
parser.add_argument('--src','-s', metavar='srcdir', required=True, help='src directory')
parser.add_argument('--out','-o', metavar="outfile", required=True, help='output file')

args = parser.parse_args()

# %%
#Load Sources
srcdir=args.src

cFile="time_series_covid19_confirmed_global.csv"
dFile="time_series_covid19_deaths_global.csv"
#cFile="time_series_19-covid-Confirmed.csv"
#dFile="time_series_19-covid-Deaths.csv"
#rFile="time_series_19-covid-Recovered.csv"

cDF = pd.read_csv(srcdir+cFile)
dDF = pd.read_csv(srcdir+dFile)
#rDF = pd.read_csv(srcdir+rFile)

# %%
dates=cDF.columns[4:]
dates


# %%
def dayData(d):
    day_cDF = cDF[['Province/State','Country/Region',d]].rename(columns={d: "Confirmed"})
    day_dDF = dDF[['Province/State','Country/Region',d]].rename(columns={d: "Deaths"})
    dayDF = pd.merge(day_cDF, day_dDF, on=['Province/State','Country/Region'], how="outer")

#    if d in rDF.columns:
#        day_rDF = rDF[['Province/State','Country/Region',d]].rename(columns={d: "Recovered"})
#        dayDF = pd.merge(dayDF, day_rDF, on=['Province/State','Country/Region'], how="outer")
#    else:
    dayDF['Recovered']=np.nan

    dayDF.insert(0,'Date',d)

    return dayDF[ (dayDF.Confirmed>0) | (dayDF.Deaths>0) | (dayDF.Recovered>0) ]

dfs = [dayData(d) for d in dates]

df = pd.concat(dfs,ignore_index=True)

# %%
df.sort_values(by=['Date','Country/Region','Province/State'])

# %%
df.to_csv(args.out, index=False)


# %%


