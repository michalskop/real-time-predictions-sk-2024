"""Download data."""

import base64
import requests
import time

# credentials
# Note: it should be in a separate file gitignored **TODO**
# however this credentials are for this day only
url = "https://volbysr.sk/media/"
username = "ZPRAVY"
password = "zvy+493-HZV8p4z"

data_path = "var/www/hlasovali.cz/real-time-predictions-sk-2024/round1/"

credentials = username + ":" + password
encoded_credentials = base64.b64encode(credentials.encode("ascii")).decode("ascii")
headers = {"Authorization": "Basic " + encoded_credentials}
r = requests.get(url, headers=headers)

files = [
  'prez2024_med_kan_okr.csv',
  'prez2024_med_kandidati.csv', 
  'prez2024_med_okresy.csv',
  'prez2024_med_suma_sr.csv',
  'prez2024_med_sv_okr.csv'
]

for f in files:
  url = "https://volbysr.sk/media/" + f
  r = requests.get(url, headers=headers)
  print(r.status_code, f)
  if r.status_code == 200:
    with open(data_path + f, 'wb') as file:
      file.write(r.content)
  time.sleep(1)
