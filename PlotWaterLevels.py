#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 10:18:25 2018

@author: crosby
"""
import matplotlib
matplotlib.use('Agg')

import getTideStationMeta
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import pickle
import os
import subprocess

fol_input = '../PointOutputs'
fol_output = '../../google-drive/SalishSeaForecasts/WaterLevels'
m2ft = 3.281
mylinewidth = 1

def plot_pred(sta,date_string,zulu_hour):
    fname = '{:s}/{:s}_twlpred.csv'.format(fol_input,sta_id[sta])
    
    df = pd.read_csv(fname)
    
    temp = df['time']
    time = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in temp]
    
    twl = df['twl pred [ft,MLLW]']
    ntr = df['NTR [ft]']
    twlE = np.zeros(len(twl))
    for tt  in range(len(twl)):
        if ntr[tt] > 0.8:
            twlE[tt] =  np.NaN
        else:
            twlE[tt] = twl[tt]
    
    plt.figure(figsize=(9,6))
    plt.plot(time,df['tide pred [ft,MLLW]'],label='Pred Tide',linewidth=mylinewidth);
    plt.plot(time,twlE,label='Pred TWL',linewidth=mylinewidth)
    plt.legend()
    plt.ylabel('Elevation [ft, MLLW]')
    plt.grid()
    plt.title('EXPERIMENTAL FORECAST: {:s}, WA                       Initialized: {:s}{:02d}00 UTC'.format(sta.title(),date_string,zulu_hour))
    plt.xticks(rotation=30)
    ax = plt.gca()
    mymin, mymax = ax.get_ylim()
    plt.yticks(np.arange(round(mymin),round(mymax),1))
    plt.ylim([mymax-4,mymax])
    plt.minorticks_on()
    plt.savefig('{:s}/{:s}.png'.format(fol_output,sta),dpi=200)


def plot_obs(sta,date_string,zulu_hour):
    fname = '{:s}/{:s}_twlpred.csv'.format(fol_input,sta_id[sta])    
    dfp = pd.read_csv(fname)
    
    fname = '{:s}/{:s}_twlobs.csv'.format(fol_input,sta_id[sta])    
    dfo = pd.read_csv(fname)
        
    temp = dfp['time']
    timep = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in temp]
    
    temp = dfo['time']
    timeo = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in temp]
    
    
    twl = dfp['twl pred [ft,MLLW]']
    ntr = dfp['NTR [ft]']
    twlE = np.zeros(len(twl))
    for tt  in range(len(twl)):
        if ntr[tt] > 0.8:
            twlE[tt] =  np.NaN
        else:
            twlE[tt] = twl[tt]
    
    plt.figure(figsize=(9,6))
    plt.plot(timeo,dfo['twl'],label='Obs TWL',linewidth=mylinewidth)
    plt.plot(timep,dfp['tide pred [ft,MLLW]'],label='Pred Tide',linewidth=mylinewidth);
    plt.plot(timep,twlE,label='Pred TWL',linewidth=mylinewidth)
    plt.legend()
    plt.ylabel('Elevation [ft, MLLW]')
    plt.grid()
    plt.xticks(rotation=30)
    plt.title('EXPERIMENTAL FORECAST: {:s}, WA                       Initialized: {:s}{:02d}00 UTC'.format(sta.title(),date_string,zulu_hour))
    ax = plt.gca()
    mymin, mymax = ax.get_ylim()
    plt.yticks(np.arange(round(mymin),round(mymax),1))
    plt.ylim([mymax-4,mymax])
    plt.minorticks_on()
    plt.savefig('{:s}/{:s}.png'.format(fol_output,sta),dpi=200)


temp = pickle.load(open('current_forecast_gdps.pkl','rb'))   
date_string = temp[0]
zulu_hour = temp[1]

# Plot predicted sties
(sta_list,sta_id,xtide_str,mllw2navd88,sta_lat,sta_lon) = getTideStationMeta.get_pred()
for sta in sta_list:
    plot_pred(sta,date_string,zulu_hour)


    
# Plot obs sties
(sta_list,sta_id,xtide_str,mllw2navd88,sta_lat,sta_lon) = getTideStationMeta.get_obs()
for sta in sta_list:
    plot_obs(sta,date_string,zulu_hour)
    
    
# Sync to Gdrive
os.chdir('../../google-drive')
griveCommand = 'grive -s SalishSeaForecasts/'
subprocess.check_call(griveCommand, shell=True)
os.chdir('../Documents/SalishSeaForecasts')    