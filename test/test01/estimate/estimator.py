"""Testing estimator producing fake results."""

import datetime
import json
import random
import pandas as pd

# path
path = "/home/michal/dev/real-time-predictions-sk-2024/test/test01/estimate/"

# data path
data_path = "../download/downloaded/"

# read data
kan_okr = pd.read_csv(path + data_path + "hlasy_okr.csv", sep="|")
sv_okr = pd.read_csv(path + data_path + "sv_okr.csv", sep="|")
source = pd.read_csv(path + "source.csv")

# CREATE FAKE RESULTS
df = source.copy()

# counted okrseks
counted = round(sv_okr['P_OKRSOK'].sum() / 5938 * 100, 2)
df['counted'] = counted

# error function, it should be 1 for 0% and 0 for 100%
error = 1 - counted / 100

# fake mean
for i in df.index:
  df.at[i, 'mean'] = max(0, source.at[i, 'mean'] * (1 + error * random.uniform(-0.3, 0.3)))
# adjust to 100%
df['mean'] = df['mean'] / df['mean'].sum() * 100

# fake 95% intervals
df['lo'] = df['mean'] - 1.96 * df['mean'] / 100 * 10 * error
df['lo'] = df['lo'].clip(lower=0)
df['hi'] = df['mean'] + 1.96 * df['mean'] / 100 * 10 * error
df['hi'] = df['hi'].clip(upper=100)

# set datetime
df['datetime'] = datetime.datetime.now().isoformat(timespec='seconds')

# set datetime-data, parse from '16.03.2019 23:15:00' to isoformat
d = datetime.datetime.strptime(sv_okr['DAT_AKT'][0], '%d.%m.%Y %H:%M:%S')
df['datetime-data'] = d.isoformat(timespec='seconds')

# save csv
df.to_csv(path + "estimates.csv", index=False)

# prepare json
df.sort_values(by='mean', ascending=False, inplace=True)
# round to 2 decimal places
df = df.round({'mean': 2, 'lo': 2, 'hi': 2})

j = {
  "info": "TEST RESULTS! Do not use as real predictions!",
  "datetime": df['datetime'][0],
  "datetime_data": df['datetime_data'][0],
  "counted": df['counted'][0],
  "candidates": []
}
j['candidates'] = df[['id', 'name', 'given_name', 'family_name', 'mean', 'lo', 'hi']].to_dict(orient='records')

# save json
with open(path + "estimates.json", 'w') as file:
  json.dump(j, file, indent=2, ensure_ascii=False)