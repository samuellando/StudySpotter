import pandas as pd
import os
import csv
import json 
import requests
import sys
import time

location = "FILL"
name = "FILL"
dsc = "FILL"
label = "FILL"
DATA_DIR = "raw_data"

"""# Import the data"""
while True:
  time.sleep(30*60) #30 minutes
  for csv in os.listdir(DATA_DIR):
    df = pd.read_csv(DATA_DIR+"/"+csv)
    df.drop(' BSSID', axis=1, inplace=True)
    df.drop(' Probed ESSIDs', axis=1, inplace=True)
    df.drop(' First time seen', axis=1, inplace=True)
    df.drop(' # packets', axis=1, inplace=True)
    df.columns = [
      'mac',
      'last_seen',
      'power'
    ]
  data = df.to_dict()
  r = requests.post("api.studyspotter.ca", data = {"location": location, "name": name, "dsc": dsc, "label": label, **data})