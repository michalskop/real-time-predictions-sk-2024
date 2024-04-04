"""Calculate the estimate of the model0."""

# Model 0: simple counting of the votes
# columns: candidate, result

import pandas as pd

# path
path = "/home/michal/dev/real-time-predictions-sk-2024/round2/estimate/"

# read data
df = pd.read_csv(path + "../extract/data.csv")

# get list of candidates, starting "votes_"
candidates_votes = list(df.columns[df.columns.str.startswith('votes_')])
candidates_ids = [c.replace("votes_", "") for c in candidates_votes]

# calculate results
if df.loc[:, candidates_votes].sum().sum() > 0:
  rx = df.loc[:, candidates_votes].sum() / df.loc[:, candidates_votes].sum().sum() * 100
else:
  rx = pd.Series([0] * len(candidates_votes), index=candidates_votes)
rx.fillna(0, inplace=True)

results = pd.DataFrame(rx).reset_index()
results.columns = ['candidate', 'result']

# save results
results.to_csv(path + "estimates_model0.csv", index=False)

print("Model 0 estimates calculated.")