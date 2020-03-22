# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import glob, sys

# %%
home=sys.path[0]
print("home is ",home)

src=home+"/../../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/*.csv"
tgt=home+"/../data/cases.csv"

print("src is ",src)
print("tgt is ",tgt)
# %%
files=glob.glob(src)

dfs = [pd.read_csv(f, parse_dates=['Last Update'], infer_datetime_format=True) for f in files]

df = pd.concat(dfs,ignore_index=True)


# %%
df.dtypes


# %%
s=df.sort_values(by=['Last Update', 'Country/Region', 'Province/State'])
s.drop_duplicates(subset =['Last Update', 'Country/Region', 'Province/State'], keep = False, inplace = True) 

# %%
s.to_csv(tgt, index=False)