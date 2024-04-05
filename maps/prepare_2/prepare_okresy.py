"""Prepare data for map of okresy."""

# map: https://app.flourish.studio/visualisation/17268823/edit

# columns: okres_code, okres, víťazný kandidát, Korčok, Pellegrini, Harabin, Matovič, ...

import pandas as pd

path = "/home/michal/dev/real-time-predictions-sk-2024/maps/"

# read data
# df_candidates = pd.read_csv(path + "prepare/prez2024_med_kandidati.csv", sep="|")
df_candidates = pd.read_csv(path + "prepare_2/candidates.csv")
candidates_ids = list(df_candidates['id'])
df_kan_okr = pd.read_csv(path + "prepare_2/prez2024_med_kan_okr.csv", sep="|")
df_okresy = pd.read_csv(path + "prepare_2/prez2024_med_okresy.csv", sep="|")

# reorder to wide format
df = df_kan_okr.pivot_table(index='OKRES', columns='PC_HL', values='P_HL_K', aggfunc='sum').reset_index()
# add percentage
df['sum'] = df.loc[:, candidates_ids].sum(axis=1)
for c in candidates_ids:
  df[c] = round(df[c] / df['sum'] * 100, 2)
# add okres names from df_okresy NOKRES
df = df.merge(df_okresy.loc[:, ['OKRES', 'NOKRES']], left_on='OKRES', right_on='OKRES', how='left')

del df['sum']
# rename columns
df.columns = ['okres_code'] + list(df_candidates['name']) + ['okres']

# find winner
df['winner'] = df.loc[:, list(df_candidates['name'])].idxmax(axis=1)

# reorder columns and save
df = df.loc[:, ['okres_code', 'okres', 'winner'] + list(df_candidates['name'])]
df.rename(columns={'winner': 'víťazný kandidát'}, inplace=True)

df.to_csv(path + "okresy-2.csv", index=False)
