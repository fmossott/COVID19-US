# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import glob
import argparse
import os, sys

# %%
home=os.path.dirname(__file__)+"/../"

# %%
if 'ipykernel_launcher' in sys.argv[0]:
    class Args: 
        pass

    args=Args()
    args.src=home+'../COVID-19/csse_covid_19_data/csse_covid_19_time_series/'
else:
    parser = argparse.ArgumentParser(description='Merge time series values')
    parser.add_argument('--src','-s', metavar='srcdir', required=True, help='src directory')

    args = parser.parse_args()

# %%
#Load Sources
srcdir=args.src

cFile="time_series_covid19_confirmed_global.csv"
dFile="time_series_covid19_deaths_global.csv"

cDF = pd.read_csv(srcdir+cFile)
dDF = pd.read_csv(srcdir+dFile)

regdata = pd.read_csv(home+'/other_info/country_data.csv')

# %%
regdata = regdata.astype({
    'Population': 'Int64'})

# %%
dates=cDF.columns[4:]
dates


# %%
def dayData(d):
    day_cDF = cDF[['Province/State','Country/Region',d]].rename(columns={d: "Confirmed"})
    day_dDF = dDF[['Province/State','Country/Region',d]].rename(columns={d: "Deaths"})
    dayDF = pd.merge(day_cDF, day_dDF, on=['Province/State','Country/Region'], how="outer")

    dayDF['Recovered']=np.nan

    dayDF.insert(0,'Date',d)

    return dayDF[ (dayDF.Confirmed>0) | (dayDF.Deaths>0) | (dayDF.Recovered>0) ]

dfs = [dayData(d) for d in dates]

df = pd.concat(dfs,ignore_index=True)

# %%
df['Date'] = pd.to_datetime(df['Date'])
# %%
df = df.groupby(['Date', 'Country/Region']).agg('sum').reset_index()

df = df.astype({
    'Confirmed': 'Int32', 
    'Recovered':'Int32',
    'Deaths':'Int32'})

# %%
df['Active Cases'] =  df['Confirmed'] - df['Deaths'] - df['Recovered']

prev = df[['Date','Country/Region','Confirmed','Deaths','Recovered','Active Cases']]
prev = prev.rename(columns={'Confirmed':'Previous Confirmed', 'Deaths':'Previous Deaths', 'Recovered':'Previous Recovered', 'Active Cases':'Previous Active'})
prev['Date'] = prev['Date']+pd.to_timedelta(1,unit='D')

prev2 = df[['Date','Country/Region','Confirmed']]
prev2 = prev2.rename(columns={'Confirmed':'Prev2 Confirmed'})
prev2['Date'] = prev2['Date']+pd.to_timedelta(2,unit='D')

prevW = df[['Date','Country/Region','Confirmed']]
prevW = prev2.rename(columns={'Confirmed':'Previous Week Confirmed'})
prevW['Date'] = prev2['Date']+pd.to_timedelta(7,unit='D')

# %%
merge=df.merge(prev, on=['Date','Country/Region'], how="left")\
    .merge(prev2, on=['Date','Country/Region'], how="left")\
    .merge(prevW, on=['Date','Country/Region'], how="left")\
    .merge(regdata, on=['Country/Region'], how='left')

# %%
merge['Daily Confirmed'] = merge['Confirmed']-merge['Previous Confirmed']
merge['Daily Deaths'] = merge['Deaths']-merge['Previous Deaths']
merge['Daily Recovered'] = merge['Recovered']-merge['Previous Recovered']
merge['Daily Active'] = merge['Active Cases']-merge['Previous Active']
merge['Previous Daily Confirmed'] = merge['Previous Confirmed']-merge['Prev2 Confirmed']
merge['Weekly Confirmed'] = merge['Confirmed']-merge['Previous Week Confirmed']

# %%
merge.sort_values(by=['Date','Country/Region'])

# %%
merge.to_csv(home+'data/world_ts.csv', index=False)

# %%
lastDF = merge.loc[merge['Date'] == merge['Date'].max()]


# %%
lastDF.to_csv(home+'data/world_last.csv', index=False)

