"""Prepare results for the map of historical regions."""

import pandas as pd

fname = "PREZ2024_kolo2_SK_tab03e.csv"

path = "/home/michal/dev/real-time-predictions-sk-2024/maps/"

# read data
df_candidates = pd.read_csv(path + "prepare_2/candidates.csv")
candidates_ids = list(df_candidates['id'])
df_data = pd.read_csv(path + "prepare_2/" + fname)

