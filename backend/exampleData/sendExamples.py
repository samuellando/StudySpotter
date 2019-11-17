import json 
import sys
from datetime import datetime
import time
import random
import requests
import numpy

URL = "http://35.232.203.137"

fp = open("nodes.json", 'r')
NODES = json.load(fp)['nodes']

CURRENT_TIME = time.time()

today = datetime.utcnow().date()
start = datetime(today.year, today.month, today.day)
START_OF_DAY = datetime.timestamp(start)

blocks = (int(CURRENT_TIME)-int(START_OF_DAY)) // 1800
i = 0

for node in NODES:
  

  n = numpy.random.normal(loc=100.00, scale=30.00, size=blocks)
  for i in range(0, blocks):
    mac = []
    last=[]
    power=[]
    for j in range(0, int(n[i])):
      mac.append("FF:FF:FF:FF")
      last.append(START_OF_DAY + 1800 * i - 5*3600)
      power.append(random.randint(-1, 20))

    df = json.dumps({"macs":mac, "last":last, "power":power})
    params = {**node, "data":df}
    params['location'] = params['id']
    del params['id']
    r = requests.post(url=URL, data=params)
    if r.json()['status'] != 'good':
      print("BAD POST")
      exit()

i = i + 1
while True:
  print(i)
  print("Sleeping...")
  time.sleep(1800)
  for node in NODES:
    mac = []
    last=[]
    power=[]

    n = numpy.random.normal(loc=100.00, scale=30.00, size=blocks)[0]

    for j in range(0, int(n)):
      mac.append("FF:FF:FF:FF")
      last.append(START_OF_DAY + 1800 * i - 5*3600)
      power.append(random.randint(-1, 20))

    df = json.dumps({"macs":mac, "last":last, "power":power})
    params = {**node, "data":df}
    params['location'] = params['id']
    del params['id']
    r = requests.post(url=URL, data=params)
    if r.json()['status'] != 'good':
      print("BAD POST")
      exit()
  i = i + 1