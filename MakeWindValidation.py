#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 18:04:52 2019

@author: crosby
"""
import pandas as pd
import noaa
import datetime
import getWindStationMeta
from scipy import io


# Load list of wind validation locations
(windlist, wind_id, wind_lat, wind_lon) = getWindStationMeta.get_obs()

fol_output = '../PointOutputs'
fol_input = '../LUTinputs'


def get_wind_obs(station):
    # --------------------- Download most recent observations ---------------------
    end_date = datetime.datetime.now() - datetime.timedelta(days=0)
    start_date = end_date - datetime.timedelta(days=4)
    
    data = noaa.get_coops_data(station,
                       start_date.strftime('%Y%m%d %H:%M'),
                       end_date.strftime('%Y%m%d %H:%M'),
                       product='wind',
                       units='metric',
                       datum='MLLW',
                       time_zone='GMT',
                       interval=False)
    
    data.pop('f',None)
    df = pd.DataFrame.from_dict(data)
    df = df.set_index('time')
    df = df.rename(index=str,columns={'d':'Direction [deg]','g':'Gusts [m/s]','s':'Speed [m/s]'})
    return df


def load_hrdps_mat(fname):
    hrdps = io.loadmat(fname)    
    # Make time axis
    start_date = datetime.datetime.strptime(hrdps['date_string'][0],'%Y%m%d') + datetime.timedelta(hours=hrdps['zulu_hour'][0][0])    
    time = [start_date+datetime.timedelta(hours=x) for x in range(48)]    
    # Convert to pandas dataframe
    df = pd.DataFrame.from_dict({'time':time,'Direction [deg]':hrdps['theta'][0],'Speed [m/s]':hrdps['u'][0]})
    df = df.set_index('time')
    return df

def get_wind_pred(station):
    # read in hrdps
    fname = '{:s}/{:s}_wind.mat'.format(fol_input,station)
    df0 = load_hrdps_mat(fname)
    fname = '{:s}/{:s}_1dayold.mat'.format(fol_input,station)
    df1 = load_hrdps_mat(fname)
    
    df = pd.concat([df1.iloc[:24], df0])
    
    return df



# Loop over stations
for sta in windlist:
    sta_id = wind_id[sta]
    
    # Get obsverations
    df_obs = get_wind_obs(sta_id)
    
    # Get predictions
    df_pred = get_wind_pred(sta_id)    
    
    # Save Obs and Pred
    df_obs.to_csv('{:s}/{:s}_wind_obs.csv'.format(fol_output,sta_id))
    df_pred.to_csv('{:s}/{:s}_wind_pred.csv'.format(fol_output,sta_id))













#url1 = 'https://www.ndbc.noaa.gov/data/realtime2/'
#url2 = 'FRDW1.txt'

#
#fname = 'temp.csv'
#cols = {'YY'  'MM' 'DD' 'hh' 'mm' 'WDIR' 'WSPD' 'GST'  'WVHT'   'DPD'   'APD' 'MWD'   'PRES'  'ATMP'  'WTMP'  'DEWP'  'VIS' 'PTDY',  'TIDE'}
#
#urllib.urlretrieve(url1+url2,fname)
#df = pd.read_csv(fname,delimiter=' ',header=2, dtype=np.float, na_values='MM',error_bad_lines=False, skip_blank_lines =True)
#df = df.drop(index=0)

#data = np.fromregex(fname,r'([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+)', dtype='float')
