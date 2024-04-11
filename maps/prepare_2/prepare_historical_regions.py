"""Prepare results for the map of historical regions."""

import pandas as pd

fname = "PREZ2024_kolo2_SK_tab03e.csv"

path = "/home/michal/dev/real-time-predictions-sk-2024/maps/"

# read data
df_candidates = pd.read_csv(path + "prepare_2/candidates.csv")
cname = 'Poradie na hlasovacom lístku'
candidates_ids = list(df_candidates['id'])
df_data = pd.read_csv(path + "prepare_2/" + fname)
df_population = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSMOKZ5govz_WYU5Lz1XCHVm1y8hNA_Sc0kecVAbBHIqwOmBVuACGeR5prvghyy0nc-Wey5_GUXfQBM/pub?gid=322316457&single=true&output=csv")

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
  df["perc_" + str(c)] = round(df[c] / df['sum'] * 100, 2)

# merge with population
df = df.merge(df_population.loc[:, ['IDN4', 'historical_region']], left_on='Kód obce', right_on='IDN4', how='left')

# pivot table over historical regions
# somehow returns error if done together
pt = df.pivot_table(index='historical_region', values=[c for c in candidates_ids], aggfunc='sum')
pt['sum'] = pt.sum(axis=1)

# percentage
for c in candidates_ids:
  pt["perc_" + str(c)] = round(pt[c] / pt['sum'] * 100, 2)

# rename columns
pt.columns = [c for c in df_candidates['name'] + ' hlasy'] + ['sum'] + [str(c) for c in df_candidates['name']]

# add winner
pt['víťaz'] = pt.loc[:, list(df_candidates['name'])].idxmax(axis=1)

# sort and save
pt.to_csv(path + "historical_regions-2.csv", index=True)