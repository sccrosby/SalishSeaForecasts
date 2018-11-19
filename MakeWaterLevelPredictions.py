#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 16:03:11 2018

@author: crosby
"""
#from scipy import io
from datetime import datetime, timedelta
import getTideStationMeta
import pickle
import time as Time
import numpy as np
import pandas as pd

gdps_input = '../gdps/PostProcessed'
tide_input = '../TidePredObs'
fol_output = '../PointOutputs'

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

# Start timer
start_time = Time.time()

# Get station list, predictions only
(sta_list, sta_id, xtide_str,mllw2navd88,sta_lat,sta_lon) = getTideStationMeta.get_pred()

sta = 'bellingham'

# Load predictions of slp
filename = '{0:s}/{1:s}_gdps_slp.pkl'.format(gdps_input,sta_id[sta])
temp = pickle.load(open(filename,'rb'))   
slp_timeC = temp[0]
slpC = temp[1]

# Load dayold predictions
filename = '{0:s}/{1:s}_gdps_slp_dayold.pkl'.format(gdps_input,sta_id[sta])
temp = pickle.load(open(filename,'rb'))   
slp_timeO = temp[0]
slpO = temp[1]

# Concat old to current
idx = slp_timeO.index(slp_timeC[0])
slp = np.append(slpO[:idx-1],slpC)
slp_time = slp_timeO[:idx-1].append(slp_timeC)

# Convert slp to water level
slpA = (slp-1.17e5) / 100
ibe = -slpA*0.12

# Load tide predictions
sta = 'bellingham'
filename = '{0:s}/{1:s}_pred_navd88.pkl'.format(tide_input,sta_id[sta])
temp = pickle.load(open(filename,'rb'))   
pred_time = temp[0]
pred = temp[1]

## Find releveant tide predictions
#time_nearest = nearest(pred_time,time_forecast)
#idx = tide.index(time_nearest)
#tide_forecast = tide[1][idx:idx+48]
#tide_time = tide[0][idx:idx+48]
#
#df_slp = pd.DataFrame.from_dict({'time':pred_time,'pred':pred})    
#df_slp = df_slp.set_index('time')
#df_slp = df_slp.resample('T') # Minute period
#df_slp = df_slp.interpolate()*10 # convert to mb
#
## Find times in predictions series that cover slp times
#test = [i for i in pred_time if i >= slp_time[0] and i <= slp_time[-1]]

# Save 

# Load wave predictions? 
print 'Total time elapsed: {0:.2f} seconds'.format(((Time.time() - start_time)))







