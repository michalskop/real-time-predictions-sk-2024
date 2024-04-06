"""Save estimates to GSheet."""

import datetime
import gspread
import pandas as pd

# source sheet
sheetkey = "1-5arnpbENvxCAN91KfFQucqZQcRR1MzdH9rNO4cTF10"
path = "/home/michal/dev/real-time-predictions-sk-2024/round2/output/"

# load data from GSheet
gc = gspread.service_account()
sh = gc.open_by_key(sheetkey)

# read data model 2
df_estimates = pd.read_csv(path + "../estimate/estimates_rich.csv")
df_info = pd.read_csv(path + "../estimate/info.csv")

# write basic info
counted = float(df_info[df_info['name'] == 'counted_president_2024-2'].iloc[-1]['value'])
dt = datetime.datetime.now().isoformat(timespec='seconds')
info = [[counted, dt]]

ws = sh.worksheet('models')
ws.update('A2', info)

# write estimates
rows = []
for i, row in df_estimates.iterrows():
  rows.append([row['result']])

ws.update('E2', rows)

# write hi and lo
rows = []
for i, row in df_estimates.iterrows():
  rows.append([row['lo'], row['hi']])

ws.update('I2', rows)

# save estimates to another row in sheet: model 2
ws = sh.worksheet('model 2')
# get last row
last_row = len(ws.get_all_values())
# prepare row
row = [counted, dt] + df_estimates['result'].tolist() + [''] + df_estimates['lo'].tolist() + [''] + df_estimates['hi'].tolist()
# write row
ws.insert_row(row, index=last_row + 1)

# read data model 0
df_estimates = pd.read_csv(path + "../estimate/estimates_model0.csv")
df_turnout = pd.read_csv(path + "../estimate/turnout.csv")

# write estimates
ws = sh.worksheet('models')

rows = []
for i, row in df_estimates.iterrows():
  rows.append([row['result']])

ws.update('G2', rows)

# save estimates to another row in sheet: model 0
ws = sh.worksheet('model 0')
# get last row
last_row = len(ws.get_all_values())
# prepare row
row = [counted, dt] + df_estimates['result'].tolist() + [''] + df_turnout['turnout'].tolist()
# write row
ws.insert_row(row, index=last_row + 1)

print("Written to Gsheet.")