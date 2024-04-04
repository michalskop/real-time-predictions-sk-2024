"""Download data from server and save them."""

import datetime
import io
import requests
import pandas as pd
import base64

# disable IP6, needed for some servers
# https://stackoverflow.com/a/72440253/1666623
requests.packages.urllib3.util.connection.HAS_IPV6 = False

path = "/home/michal/dev/real-time-predictions-sk-2024/round2/download/"

data_path = "downloaded/"

# server_url = "https://www.matop.sk/data/su/"  # testing server 1
# server_url = "http://localhost:8000/" # local testing server
# server_url = "https://hlasovali.cz/real-time-predictions-sk-2024/round1/" # backup server with data
server_url = "https://volbysr.sk/media/"  # real server

# credentials
# Note: it should be in a separate file gitignored **TODO**
# however this credentials are for this day only

username = "ZPRAVY"
password = "zvy+493-HZV8p4z"

# setting headers
credentials = username + ":" + password
encoded_credentials = base64.b64encode(credentials.encode("ascii")).decode("ascii")
headers = {"Authorization": "Basic " + encoded_credentials}

# all files
# files = ['hlasy_okr', 'sv_okr']
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

print("Download done.")
# time.sleep(20)