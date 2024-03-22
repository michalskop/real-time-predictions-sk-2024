"""Download data from test server and save them."""

# import base64
import datetime
import io
import requests
import pandas as pd
import base64
# import time

path = "/home/michal/dev/real-time-predictions-sk-2024/test/test02/download/"

data_path = "downloaded/"

server_url = "https://www.matop.sk/data/su/"
# server_url = "https://volbysr.sk/media/"

# credentials
# Note: it should be in a separate file gitignored **TODO**
# however this credentials are for this day only

username = "ZPRAVY"
password = "zvy+493-HZV8p4z"

credentials = username + ":" + password
encoded_credentials = base64.b64encode(credentials.encode("ascii")).decode("ascii")
headers = {"Authorization": "Basic " + encoded_credentials}

# all files
# files = ['nrsr2023_med_kan_sr', 'nrsr2023_med_kandidati', 'nrsr2023_med_okresy', 'nrsr2023_med_ps_okr', 'nrsr2023_med_psubjekty', 'nrsr2023_med_suma_sr', 'nrsr2023_med_sv_okr']
# important files only
# files = ['nrsr2023_med_ps_okr', 'nrsr2023_med_sv_okr', 'nrsr2023_med_suma_sr']
# changing file only
# files = ['nrsr2023_med_kan_sr', 'nrsr2023_med_ps_okr', 'nrsr2023_med_suma_sr', 'nrsr2023_med_sv_okr']
files = ['hlasy_okr', 'sv_okr']
files = ['prez2024_med_kan_okr', 'prez2024_med_sv_okr']

t = datetime.datetime.now().isoformat(timespec='seconds')

for f in files:
  url = server_url + f + ".csv"
  r = requests.get(url, headers=headers)
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