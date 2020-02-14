#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:08:29 2020

@author: crosby
"""

import json
import pickle
from datetime import datetime, timedelta

# Manifest location
data_fol = '/home/crosby/Documents/usgstidal/data-packager/datafolder'

# Load in manifest
with open('{:s}/manifest_backup.json'.format(data_fol)) as f:
    data = json.load(f)
    
# See what's inside       
# print(data)

# Get current forecast
temp = pickle.load(open('current_forecast.pkl','rb'))   
date_string = temp[0]
zulu_hour = temp[1]
time = datetime.strptime(date_string,'%Y%m%d')
time = time + timedelta(hours=zulu_hour) - timedelta(hours=8)

# update data time
data['startDateTime'] = time.strftime('%Y-%m-%d %H:%M:%S')

# Write new manifest
with open('{:s}/manifest.json'.format(data_fol), 'w') as f:
    json.dump(data,f,ensure_ascii=False,indent=2)