# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import glob
import re
import datetime
import argparse
import os, sys

# %%
home=os.path.dirname(__file__)+"/../"

# %%
if 'ipykernel_launcher' in sys.argv[0]:
    class Args: 
        pass

    args=Args()
    args.src=home+'../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
else:
    parser = argparse.ArgumentParser(description='Merge daily reports files')
    parser.add_argument('--src','-s', metavar='srcdir', required=True, help='src directory')
    
    args = parser.parse_args()

# %%
files=glob.glob(args.src + "/*.csv")
files.sort()


regdata = pd.read_csv(home+'/other_info/uscounties_data.csv')

# %%
regdata = regdata.astype({
    'Population': 'Int64'})

# %%
def filedate(f):
    matchObj = re.match( r'^.*\/(\d{2})-(\d{2})-(\d{4}).csv$', f, re.M)
    result=None
    if matchObj:
        result= datetime.datetime(int(matchObj.group(3)), int(matchObj.group(1)), int(matchObj.group(2)))
    return result

# %%
def read_csv(d, f):
    df = pd.read_csv(f);
    df.insert(0, 'Date', d)

    df = df.rename(columns={'Province_State': 'Province/State', 'Country_Region': 'Country/Region', 'Lat': 'Latitude', 'Long_': 'Longitude', 'Last_Update:': 'Last Update'})
    df = df[(df['Country/Region']=='US') & ((df.Confirmed>0) | (df.Deaths>0) | (df.Recovered>0)) ]

    return df

dfs = [read_csv(filedate(f), f) for f in files]

# %%
df = pd.concat(dfs,ignore_index=True)

# %%
df['Date'] = pd.to_datetime(df['Date'])
# %%
df = df.groupby(['Date', 'Country/Region', 'Province/State', 'Admin2']).agg('sum').reset_index()

df = df.astype({
    'Confirmed': 'Int32', 
    'Recovered':'Int32',
    'Deaths':'Int32'})

# %%
df['Active Cases'] =  df['Confirmed'] - df['Deaths'] - df['Recovered']

prev = df[['Date','Country/Region','Province/State','Admin2','Confirmed','Deaths','Recovered','Active Cases']]
prev = prev.rename(columns={'Confirmed':'Previous Confirmed', 'Deaths':'Previous Deaths', 'Recovered':'Previous Recovered', 'Active Cases':'Previous Active'})
prev['Date'] = prev['Date']+pd.to_timedelta(1,unit='D')

prev2 = df[['Date','Country/Region','Province/State','Admin2','Confirmed']]
prev2 = prev2.rename(columns={'Confirmed':'Prev2 Confirmed'})
prev2['Date'] = prev2['Date']+pd.to_timedelta(2,unit='D')

# %%
merge=df.merge(prev, on=['Date','Country/Region','Province/State','Admin2'], how="left")\
    .merge(prev2, on=['Date','Country/Region','Province/State','Admin2'], how="left")\
    .merge(regdata, on=['Country/Region','Province/State','Admin2'], how='left')

# %%
def clip(s):
    s [ s<0 ] = 0
    return s

merge['Daily Confirmed'] = clip(merge['Confirmed']-merge['Previous Confirmed'])
merge['Daily Deaths'] = clip(merge['Deaths']-merge['Previous Deaths'])
merge['Daily Recovered'] = clip(merge['Recovered']-merge['Previous Recovered'])
merge['Daily Active'] = merge['Active Cases']-merge['Previous Active']
merge['Previous Daily Confirmed'] = clip(merge['Previous Confirmed']-merge['Prev2 Confirmed'])
merge = merge.drop(columns=['Active'])

# %%
merge = merge.sort_values(by=['Date','Country/Region','Province/State','Admin2'])

# %%
maxDate = merge['Date'].max();
minDate = maxDate - pd.to_timedelta(15,unit='D');

# %%
lastWeeks = merge.loc[merge['Date'] >= minDate]
lastWeeks.to_csv(home+'data/uscounties_ts', index=False)

# %%
lastDF = merge.loc[merge['Date'] == maxDate]


# %%
lastDF.to_csv(home+'data/uscounties_last', index=False)

# %%
unfound = lastDF[(lastDF['Population'].isna())]
unfound = unfound[(unfound['Admin2']!='Unassigned')]
unfound = unfound[(~unfound['Admin2'].str.startswith('Out of '))]

if unfound.size > 0:
    print(unfound)

