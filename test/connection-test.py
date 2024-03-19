"""Test connection and download trial data."""

import base64
import requests
import time

# disable IP6, needed for some servers
# https://stackoverflow.com/a/72440253/1666623
requests.packages.urllib3.util.connection.HAS_IPV6 = False

# credentials
# Note: it should be in a separate file gitignored **TODO**
# however this credentials are for this day only
url = "https://volbysr.sk/media/"
username = "ZPRAVY"
password = "zvy+493-HZV8p4z"

data_path = "test/downloaded/"

credentials = username + ":" + password
encoded_credentials = base64.b64encode(credentials.encode("ascii")).decode("ascii")
headers = {"Authorization": "Basic " + encoded_credentials}
r = requests.get(url, headers=headers)

print(r.status_code)

# download trial data
files = ['prez2024_k1_med_popis.pdf',
  'prez2024_k2_med_popis.pdf',
  'prez2024_med_kan_okr.csv',
  'prez2024_med_kandidati.csv', 
  'prez2024_med_okresy.csv',
  'prez2024_med_suma_sr.csv',
  'prez2024_med_sv_okr.csv']

files = [
  'prez2024_med_kan_okr.csv',
  'prez2024_med_kandidati.csv', 
  'prez2024_med_okresy.csv',
  'prez2024_med_suma_sr.csv',
  'prez2024_med_sv_okr.csv'
]

# stav
stav = "stav2/"

for f in files:
  url = "https://volbysr.sk/media/" + stav + f
  r = requests.get(url, headers=headers)
  print(r.status_code, f)
  with open(data_path + stav + f, 'wb') as file:
    file.write(r.content)
  time.sleep(1)