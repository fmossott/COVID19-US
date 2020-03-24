# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import glob
import re
import datetime
import argparse



# %%
parser = argparse.ArgumentParser(description='Merge daily reports files')
parser.add_argument('--src','-s', metavar='srcdir', required=True, help='src directory')
parser.add_argument('--out','-o', metavar="outfile", required=True, help='output file')

args = parser.parse_args()

# %%
files=glob.glob(args.src + "/*.csv")
files.sort()

# %%
def filedate(f):
    matchObj = re.match( r'^.*\/(\d{2})-(\d{2})-(\d{4}).csv$', f, re.M)
    result=None
    if matchObj:
        result= datetime.datetime(int(matchObj.group(3)), int(matchObj.group(1)), int(matchObj.group(2)))
    return result

# %%
#dfs = [pd.read_csv(f, parse_dates=['Last Update'], infer_datetime_format=True) for f in files]

def read_csv(d, f):
    df = pd.read_csv(f);
    df.insert(0, 'Date', d)

    df = df.rename(columns={'Province_State': "Province/State", 'Country_Region': 'Country/Region', 'Lat': 'Latitude', 'Long_': 'Longitude', 'Last_Update:': 'Last Update'})
    return df

dfs = [read_csv(filedate(f), f) for f in files]

# %%
df = pd.concat(dfs,ignore_index=True)

# %%
s=df.sort_values(by=['Date', 'Country/Region', 'Province/State', 'Admin2'])

# %%
start_cols=['Date', 'Country/Region', 'Province/State', 'Admin2']
s=s[start_cols + [c for c in df if c not in start_cols]]


# %%
s.to_csv(args.out, index=False)