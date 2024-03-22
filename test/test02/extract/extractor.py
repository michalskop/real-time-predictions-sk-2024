"""Extracts data from the downloaded SUSR files."""

# prepares extracted_data.csv:
# columns: okres_code, polling_stations, counted_polling_stations, counted, voted, counted_voted, voters, votes_1, ...

import pandas as pd

# path
path = "/home/michal/dev/real-time-predictions-sk-2024/test/test02/extract/"

# read source files
df_okresy = pd.read_csv(path + "okresy.csv")
df_candidates = pd.read_csv(path + "candidates.csv")

# read results
