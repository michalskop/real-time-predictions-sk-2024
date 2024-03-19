"""Download data from test server and save them."""

# import base64
import datetime
import io
import requests
import pandas as pd
# import time

path = "/home/michal/dev/real-time-predictions-sk-2024/test/test01/download/"

data_path = "downloaded/"

# all files
# files = ['nrsr2023_med_kan_sr', 'nrsr2023_med_kandidati', 'nrsr2023_med_okresy', 'nrsr2023_med_ps_okr', 'nrsr2023_med_psubjekty', 'nrsr2023_med_suma_sr', 'nrsr2023_med_sv_okr']
# important files only
# files = ['nrsr2023_med_ps_okr', 'nrsr2023_med_sv_okr', 'nrsr2023_med_suma_sr']
# changing file only
# files = ['nrsr2023_med_kan_sr', 'nrsr2023_med_ps_okr', 'nrsr2023_med_suma_sr', 'nrsr2023_med_sv_okr']
files = ['hlasy_okr', 'sv_okr']

t = datetime.datetime.now().isoformat(timespec='seconds')

for f in files:
  url = "https://www.matop.sk/data/su/" + f + ".csv"
  r = requests.get(url)
  print(url, r.status_code)
  if r.status_code == 200:
    # save only if correct CSV
    try:
      x = pd.read_csv(io.StringIO(r.content.decode('utf-8')), sep="|")
      x.to_csv(path + data_path + f + ".csv", index=False, sep="|")
      # archive
      x.to_csv(path + data_path + "archive/" + f + "_" + t + ".csv", index=False, sep="|")

    except:
      print("Error: file not CSV.")
      pass

# time.sleep(20)