"""Extracts data from the downloaded SUSR files."""

# prepares extracted_data.csv:
# columns: okres_code, polling_stations, counted_polling_stations, counted, voted, counted_voted, voters, votes_1, ...

# it should stop with an error if there are no downloaded files

import datetime
import pandas as pd

# path
path = "/home/michal/dev/real-time-predictions-sk-2024/round2/extract/"
datapath = "../download/"

# read source files
df_okresy = pd.read_csv(path + "okresy.csv")
df_candidates = pd.read_csv(path + "candidates.csv")

# read results
files = ['prez2024_med_kan_okr', 'prez2024_med_sv_okr']
df_kan_okr = pd.read_csv(path + datapath + "downloaded/" + files[0] + ".csv", sep="|")
df_sv_okr = pd.read_csv(path + datapath + "downloaded/" + files[1] + ".csv", sep="|")

# prepare empty dataframe
df = df_okresy.loc[:, ['okres_code', 'polling_stations', 'last_voters']]

# add columns from df_sv_okr
df = df.merge(df_sv_okr.loc[:, ['OKRES', 'P_OKRSOK', 'P_ZAP', 'P_HL']], left_on='okres_code', right_on='OKRES', how='left')
del df['OKRES']
df.columns = ['okres_code', 'polling_stations', 'last_voters', 'counted_polling_stations', 'voters', 'counted_voted']

# pivot table for votes
pt = df_kan_okr.pivot_table(index='OKRES', columns='PC_HL', values='P_HL_K', aggfunc='sum').reset_index()

# add columns from pt
for c in df_candidates['id']:
  if c not in pt.columns:
    pt[c] = 0
  df = df.merge(pt.loc[:, ['OKRES', c]], left_on='okres_code', right_on='OKRES', how='left')
  df.rename(columns={c: 'votes_' + str(c)}, inplace=True)
  del df['OKRES']
  
df.fillna(0, inplace=True)

# calculate voted
df['voted'] = df.loc[:, ['votes_' + str(c) for c in df_candidates['id']]].sum(axis=1)

# calculate counted (counted_voted is actually counted_voters, but it is not used in the model)
df['counted'] = round(df['counted_polling_stations'] / df['polling_stations'] * 100, 2)
df['counted_voted'] = round(df['voters'] / df['last_voters'] * 100, 2)

# reorder and save
df = df.loc[:, ['okres_code', 'polling_stations', 'counted_polling_stations', 'counted', 'voted','counted_voted', 'voters'] + ['votes_' + str(c) for c in df_candidates['id']]]

df.to_csv(path + "data.csv", index=False)

# prepare info file with datetime of updates
# format: 05.03.2024 11:45:00
if len(df_kan_okr) == 0:
  dt1 = '2024-04-06T20:00:00'
else:
  dt1 = datetime.datetime.strptime(df_kan_okr['DAT_AKT'][0], '%d.%m.%Y %H:%M:%S').isoformat(timespec='seconds')
if len(df_sv_okr) == 0:
  dt2 = '2024-04-06T20:00:00'
else:
  dt2 = datetime.datetime.strptime(df_sv_okr['DAT_AKT'][0], '%d.%m.%Y %H:%M:%S').isoformat(timespec='seconds')

info = [
  {
    'name': files[0],
    'datetime': dt1
  },
  {
    'name': files[1],
    'datetime': dt2
  }
]
pd.DataFrame(info).to_csv(path + "info.csv", index=False)

print("Data extracted.")