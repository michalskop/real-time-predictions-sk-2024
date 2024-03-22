"""Prepare outputs."""

import datetime
import pandas as pd
import json
import math

# path
path = "/home/michal/dev/real-time-predictions-sk-2024/round1/output/"

# read data
df_estimates = pd.read_csv(path + "../estimate/estimates_rich.csv")
df_info = pd.read_csv(path + "../estimate/info.csv")
df_candidates = pd.read_csv(path + "candidates.csv")

# prepare output json
output = {
  "info": "REAL RESULTS! Godspeed to the model!",
  "datetime": datetime.datetime.now().isoformat(timespec='seconds'),
  "datetime-model": df_info[df_info['name'] == 'estimating_president_2024-1'].iloc[-1]['value'],
  "datetime-data": df_info[df_info['name'] == 'prez2024_med_kan_okr'].iloc[-1]['value'],
  "counted": round(float(df_info[df_info['name'] == 'counted_president_2024-1'].iloc[-1]['value']), 2),
  "candidates": []
}
# add sorted candidates
df_candidates['candidate'] = 'votes_' + df_candidates['id'].astype(str)
# merge with estimates
df = df_estimates.merge(df_candidates, on='candidate')
df = df.sort_values(by='result', ascending=False)
# add candidates
for i, row in df.iterrows():
  output['candidates'].append({
    "id": row['id'],
    "name": row['name'],
    "given_name": row['given_name'],
    "fimily_name": row['family_name'],
    "mean": round(row['result'], 2),
    "hi": math.ceil(row['hi'] * 100) / 100,
    "lo": math.floor(row['lo'] * 100) / 100
  })

# save output
with open(path + "estimates.json", "w") as f:
  json.dump(output, f, indent=2, ensure_ascii=False)

# archive
with open(path + "archive/estimates_" + datetime.datetime.now().isoformat(timespec='seconds') + ".json", "w") as f:
  json.dump(output, f, indent=2, ensure_ascii=False)

print("Output done.")