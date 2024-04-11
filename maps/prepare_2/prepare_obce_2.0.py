"""Prepare data for map of obce."""

'''
Absolute numbers of votes for each candidate in each municipality.
'''

# source data: https://volbysr.sk/sk/subory_na_stiahnutie.html
# tab_O3e.csv

# previous: https://volby.statistics.sk/nrsr/nrsr2023/sk/subory_na_stiahnutie.html

# solve Bratislava and Košice:
# Bratislava: Kód okresu 101, 102, 103, 104, 105 -> 582000
# Košice: Kód okresu 802, 803, 804, 805 -> 599981

import pandas as pd

fname = "PREZ2024_kolo2_SK_tab03e.csv"
fname2 = "PREZ2024_kolo2_SK_tab02e.csv"
cname = 'Poradie na hlasovacom lístku'
path = "/home/michal/dev/real-time-predictions-sk-2024/maps/"

# read data
df_candidates = pd.read_csv(path + "prepare_2/candidates.csv")
candidates_ids = list(df_candidates['id'])
df_data = pd.read_csv(path + "prepare_2/" + fname)
df_source_points = pd.read_csv(path + "prepare_2/source_obce_points.csv")
df_source_regions = pd.read_csv(path + "prepare_2/source_obce_regions.csv")
df_data2 = pd.read_csv(path + "prepare_2/" + fname2)

# filter Bratislava and Košice
df_data_BAKE = df_data[df_data['Kód okresu'].isin([101, 102, 103, 104, 105, 802, 803, 804, 805])]
df_data_notBAKE = df_data[~df_data['Kód okresu'].isin([101, 102, 103, 104, 105, 802, 803, 804, 805])]

df_data2_BAKE = df_data2[df_data2['Kód okresu'].isin([101, 102, 103, 104, 105, 802, 803, 804, 805])]
df_data2_notBAKE = df_data2[~df_data2['Kód okresu'].isin([101, 102, 103, 104, 105, 802, 803, 804, 805])]

mp = {101: 582000, 102: 582000, 103: 582000, 104: 582000, 105: 582000, 802: 599981, 803: 599981, 804: 599981, 805: 599981}
df_data_BAKE['Kód obce'] = df_data_BAKE['Kód okresu'].map(mp)
df_BAKE = df_data_BAKE.pivot_table(index='Kód obce', columns=cname, values='Počet platných hlasov', aggfunc='sum').reset_index().fillna(0)
df_notBAKE = df_data_notBAKE.pivot_table(index='Kód obce', columns=cname, values='Počet platných hlasov', aggfunc='sum').reset_index().fillna(0)

df_data2_BAKE['Kód obce'] = df_data2_BAKE['Kód okresu'].map(mp)
df_BAKE_voters = df_data2_BAKE.pivot_table(index='Kód obce', values='Počet zapísaných voličov', aggfunc='sum').reset_index().fillna(0)
df_notBAKE_voters = df_data2_notBAKE.pivot_table(index='Kód obce', values='Počet zapísaných voličov', aggfunc='sum').reset_index().fillna(0)

# concatenate
df = pd.concat([df_BAKE, df_notBAKE])
df_voters = pd.concat([df_BAKE_voters, df_notBAKE_voters])

# sum
df['voted'] = df.loc[:, candidates_ids].sum(axis=1)

# rename columns
df.columns = ['obec_code'] + list(df_candidates['name']) + ['voted']
df_voters.columns = ['obec_code', 'voters']

# merge with voters
df = df.merge(df_voters, on='obec_code', how='left')

# turnout
df['turnout'] = round(df['voted'] / df['voters'] * 100, 2)

# sort and save
df.sort_values('obec_code', inplace=True)

# merge to sources and save
df_points = df_source_points.merge(df, right_on='obec_code', left_on='IDN4', how='left')
df_regions = df_source_regions.merge(df, right_on='obec_code', left_on='IDN4', how='left')

df_points.to_csv(path + "obce_points-2_votes.csv", index=False)
df_regions.to_csv(path + "obce_regions-2_votes.csv", index=False)