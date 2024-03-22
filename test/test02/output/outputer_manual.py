"""Manual outputer."""

# for emegrency use and testing

import json
import pandas as pd
import datetime

path = "/home/michal/dev/real-time-predictions-sk-2024/test/test02/output/"

df = pd.read_csv(path + "output_manual.csv")
df.fillna("", inplace=True)

# prepare output json
estimate = {
  "info": df['info'][0],
  "datetime": df['datetime'][0],
  "datetime-model": df['datetime-model'][0],
  "datetime-data": df['datetime-data'][0],
  "counted": df['counted'][0],
  "candidates": []
}

# add candidates, sort them first
df.sort_values(by='mean', ascending=False, inplace=True)

for i, row in df.iterrows():
  estimate['candidates'].append({
    "id": row['id'],
    "name": row['name'],
    "given_name": row['given_name'],
    "family_name": row['family_name'],
    "mean": row['mean'],
    "hi": row['hi'],
    "lo": row['lo']
  })

# save output
with open(path + "estimates_manual.json", "w") as f:
  json.dump(estimate, f, indent=2, ensure_ascii=False)

# archive
with open(path + "archive/estimates_manual_" + datetime.datetime.now().isoformat(timespec='seconds') + ".json", "w") as f:
  json.dump(estimate, f, indent=2, ensure_ascii=False)