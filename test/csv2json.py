"""Convert CSV to JSON."""

import pandas as pd
import numpy as np
import json

# Open the CSV
df = pd.read_csv('test/estimates-test.v1.csv')

# sort by mean
df = df.sort_values(by='mean', ascending=False).reset_index()

# create output
output = {
  "candidates": [],
}

output['datetime'] = df['datetime'][0]
output['datetime_data'] = df['datetime-data'][0]
output['counted'] = df['counted'][0]
for i in range(len(df)):
  output['candidates'].append({
    "id": df['id'][i],
    "name": df['name'][i],
    "given_name": df['given_name'][i],
    "family_name": df['family_name'][i],
    "mean": df['mean'][i],
    "lo": df['lo'][i],
    "hi": df['hi'][i]
  })

# convert numpy.int64 to int because json doesn't like numpy.int64
def default(o):
    if isinstance(o, np.int64): return int(o)  
    raise TypeError

# write to file
with open('test/estimates-test.v1.json', 'w') as f:
  json.dump(output, f, indent=2, ensure_ascii=False, default=default)