import pandas as pd
import os
import csv
import json 
import sys

"""# Import the data"""

DATA_DIR = "raw_data"
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

data_dictionary = df.to_dict() 

from datetime import datetime
# unix_time return the input time - A hours in seconds
def unix_time(dt):
    dt = datetime.strptime(dt, " %Y-%m-%d %H:%M:%S")
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() - 5*3600

e = unix_time(data_dictionary['last_seen'][0])

for i in range(0,len(df)-1):
  stamp = unix_time(data_dictionary['last_seen'][i])
  if time.time() - 24*60*60 > stamp:
    del data_dictionary['mac'][i]
    del data_dictionary['last_seen'][i]
    del data_dictionary['power'][i]
  else:
    data_dictionary['last_seen'][i] = stamp