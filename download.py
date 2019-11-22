import requests
import json

URL = 'http://35.232.203.137'

locs = requests.get(URL)
locs = locs.json()['locations']


datas = {}
for loc in locs:
  data = requests.get(URL+"?location="+loc['id'])
  data = data.json()

  datas[loc['id']] = data

print(json.dumps(datas))
