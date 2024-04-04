"""Output result to a table for a chart."""

# 2 candidates
# https://app.flourish.studio/visualisation/17430516/edit

import pandas as pd

# path
path = "/home/michal/dev/real-time-predictions-sk-2024/round2/output/"

# read data
df_estimates = pd.read_csv(path + "../estimate/estimates_rich.csv")
df_candidates = pd.read_csv(path + "candidates.csv")
df_estimates['id'] = df_estimates['candidate'].str.replace("votes_", "").astype(int)

# merge data
dfx = df_estimates.merge(df_candidates, on='id', how='left', suffixes=['', '_initial']).sort_values(by='result', ascending=False)

df = dfx.loc[:, ['family_name', 'hi', 'result', 'lo']].round(1)

# 2 only
df = df.head(2)
df2 = df.copy()

# add first row ['Strana', 'jistý zisk', 'jistý zisk', 'jistý zisk']
df = pd.concat([pd.DataFrame([['Strana', 'jistý zisk', 'jistý zisk', 'jistý zisk']], columns=df.columns), df], ignore_index=True)

# add rows below: candidates name, '', result, ''
df2['hi'] = ''
df2['lo'] = ''
df = pd.concat([df, df2], ignore_index=True)

output = df.T

# save output
output.to_csv(path + "prediction_bar_chart_flourish.csv", index=False, header=False)
