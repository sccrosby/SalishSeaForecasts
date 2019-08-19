#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 16:03:11 2018

@author: crosby
"""
#from scipy import io
import getTideStationMeta
import pickle
import time as Time
import numpy as np
import pandas as pd
from datetime import datetime
import urllib
import os

gdps_input = '../gdps/PostProcessed'
tide_input = '../TidePredObs'
fol_output = '../PointOutputs'
m2ft = 3.281

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def get_obs(sta_id,start_date,end_date):
    url1 = 'https://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&application=NOS.COOPS.TAC.WL&station={:s}'.format(sta_id)
    url2 = '&begin_date={:s}&end_date={:s}&datum=MLLW&units=english&time_zone=GMT&format=csv'.format(start_date.strftime('%Y%m%d'),end_date.strftime('%Y%m%d'))
    
    # Download File to string
    fname = 'temp.csv'
    urllib.urlretrieve(url1+url2,fname)
    df_obs = pd.read_csv(fname)
    os.remove(fname)
    
    # Create new data frame to output
    df = pd.DataFrame()
    
    # Add time and observations
    df['time'] = [datetime.strptime(tt,'%Y-%m-%d %H:%M') for tt in df_obs['Date Time']]
    df['twl'] = df_obs[' Water Level']
    
    return df

def make_twl_pred_df(sta):    
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
    slp = np.concatenate((slpO[0][:idx-1],slpC[0]),axis=0)
    slp_time = slp_timeO[:idx-1] + slp_timeC[:]
    
    # Convert slp to water level
    slp = slp/100
    slpA = slp-1017
    ibe = -slpA*12 #[mm]
    ibe = ibe/1000 # [m]
    
    # Load tide predictions
    filename = '{0:s}/{1:s}_pred_navd88.pkl'.format(tide_input,sta_id[sta])
    temp = pickle.load(open(filename,'rb'))   
    pred_time = temp[0]
    pred = temp[1]
    
    # Shorten onto slp_time (hourly)
    idx = pred_time.index(slp_time[0])
    idx2 = pred_time.index(slp_time[-1])+1
    pred = pred[idx:idx2]
    pred_time = pred_time[idx:idx2]
    
    # Generate databases for time interping
    df_pred = pd.DataFrame.from_dict({'time':pred_time,'pred':pred})
    df_pred = df_pred.set_index('time')
    df_pred = df_pred.resample('H').ffill() # Minute period
    
    df_ibe = pd.DataFrame.from_dict({'time':slp_time,'ibe':ibe})
    df_ibe = df_ibe.set_index('time')
    df_ibe = df_ibe.resample('H').interpolate() # Minute period
    
    df_out = pd.concat([df_pred, df_ibe],axis=1)
    df_out['twl pred'] = df_out['pred'] + df_out['ibe']
    
    # Convert to feet in MLLW, ft
    df_out['pred'] = (df_out['pred'] + mllw2navd88[sta])*m2ft
    df_out['ibe'] =(df_out['ibe'])*m2ft
    df_out['twl pred'] =(df_out['twl pred'] + mllw2navd88[sta])*m2ft
    
    df_out = df_out.rename(index=str, columns={'pred':'tide pred [ft,MLLW]','ibe':'NTR [ft]','twl pred':'twl pred [ft,MLLW]'})
    
    return df_out
   


# Start timer
start_time = Time.time()

# ---------------------- First get predictions at all stations -----------------
# Get station list, predictions only
(sta_list,sta_id,xtide_str,mllw2navd88,sta_lat,sta_lon) = getTideStationMeta.get_all()

for sta in sta_list:
    df = make_twl_pred_df(sta)
    df.to_csv('{:s}/{:s}_twl_pred.csv'.format(fol_output,sta_id[sta]))


# save start date for observation bounds
start_date = datetime.strptime(df.index[0],'%Y-%m-%d %H:%M:%S')

# ------------------------- Second get observations where avail ------------
(sta_list,sta_id,xtide_str,mllw2navd88,sta_lat,sta_lon) = getTideStationMeta.get_obs()
for sta in sta_list:    
    df = get_obs(sta_id[sta],start_date,datetime.utcnow())
    df.set_index('time')
    df.rename(columns={'twl':'twl obs [ft,MLLW]'})    
    df.to_csv('{:s}/{:s}_twl_obs.csv'.format(fol_output,sta_id[sta]))
#    ax = df.plot()
#    fig = ax.get_figure()
#    fig.savefig('{:s}/{:s}.png'.format(fol_output,sta_id[sta]))

#import noaaTides
#myproduct = 'hourly_height'
#noaa = noaaTides.get_coops_data(station=sta_id[sta],
#                   start_date=datetime.strftime(slp_time[0],'%Y%m%d %H:%M'),
#                   end_date=datetime.strftime(slp_time[-2],'%Y%m%d %H:%M'),
#                   product=myproduct,
#                   units='metric',
#                   datum='MLLW',
#                   time_zone='GMT',
#                   interval=False)





print 'Total time elapsed: {0:.2f} seconds'.format(((Time.time() - start_time)))


#df_out.plot()


#myproduct = 'predictions'
#noaa = noaaTides.get_coops_data(station=sta_id[sta],
#                   start_date=datetime.strftime(slp_time[0],'%Y%m%d %H:%M'),
#                   end_date=datetime.strftime(slp_time[-2],'%Y%m%d %H:%M'),
#                   product=myproduct,
#                   units='metric',
#                   datum='MLLW',
#                   time_zone='GMT',
#                   interval=False)

    
    
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








