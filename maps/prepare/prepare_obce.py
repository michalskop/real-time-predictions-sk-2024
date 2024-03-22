"""Prepare data for map of obce."""

# source data: https://volbysr.sk/sk/subory_na_stiahnutie.html
# tab_O3e.csv

# previous: https://volby.statistics.sk/nrsr/nrsr2023/sk/subory_na_stiahnutie.html

# solve Bratislava and Košice:
# Bratislava: Kód okresu 101, 102, 103, 104, 105 -> 582000
# Košice: Kód okresu 802, 803, 804, 805 -> 599981

import pandas as pd

fname = "NRSR2023_SK_tab03e.csv"
cname = 'Číslo politického subjektu'

path = "/home/michal/dev/real-time-predictions-sk-2024/maps/"

# read data
df_candidates = pd.read_csv(path + "prepare/candidates.csv")
candidates_ids = list(df_candidates['id'])
df_data = pd.read_csv(path + "prepare/" + fname)

# filter Bratislava and Košice
df_data_BAKE = df_data[df_data['Kód okresu'].isin([101, 102, 103, 104, 105, 802, 803, 804, 805])]
df_data_notBAKE = df_data[~df_data['Kód okresu'].isin([101, 102, 103, 104, 105, 802, 803, 804, 805])]

mp = {101: 582000, 102: 582000, 103: 582000, 104: 582000, 105: 582000, 802: 599981, 803: 599981, 804: 599981, 805: 599981}
df_data_BAKE['Kód obce'] = df_data_BAKE['Kód okresu'].map(mp)
df_BAKE = df_data_BAKE.pivot_table(index='Kód obce', columns=cname, values='Počet platných hlasov', aggfunc='sum').reset_index().fillna(0)

df_notBAKE = df_data_notBAKE.pivot_table(index='Kód obce', columns=cname, values='Počet platných hlasov', aggfunc='sum').reset_index().fillna(0)

# concatenate
df = pd.concat([df_BAKE, df_notBAKE])

# add percentage
df['sum'] = df.loc[:, candidates_ids].sum(axis=1)
for c in candidates_ids:
  df[c] = round(df[c] / df['sum'] * 100, 2)

df.fillna(0, inplace=True)
df.drop(columns=['sum'], inplace=True)

# for development only:
df = df.loc[:, ['Kód obce'] + list(df_candidates['id'])]

# rename columns
df.columns = ['obec_code'] + list(df_candidates['name'])

# add column with winner
df['Víťazný kandidát'] = df.loc[:, list(df_candidates['name'])].idxmax(axis=1)

# sort and save
df.sort_values('obec_code', inplace=True)
df.to_csv(path + "obce.csv", index=False)
