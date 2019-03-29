#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 15:57:11 2018

Retrieve location list for stations

@author: crosby
"""

# Full location info 
Lsta_id = {
        'bellingham':'9449211',
        'sneeoosh':'9448576',
        'kayakpoint':'9448043',
        'nisqually':'9446828',
        'tacoma':'9446484',
        'seattle':'9447130',
        'porttownsend':'9444900',
        'cherrypoint':'9449424'}

Lxtide_str = {
        'bellingham':'Bellingham, Bellingham Bay, Washington',
        'sneeoosh':'Sneeoosh Point, Washington',
        'kayakpoint':'Kayak Point, Washington',
        'nisqually':'Dupont Wharf, Nisqually Reach, Puget Sound, Washington',
        'tacoma':'Tacoma, Commencement Bay, Sitcum Waterway, Puget Sound, Washington',
        'seattle':'Seattle, Puget Sound, Washington',
        'porttownsend':'Port Townsend (Point Hudson), Admiralty Inlet, Washington',
        'cherrypoint':'Cherry Point, Strait of Georgia, Washington'}

Lmllw2navd88 = {
        'bellingham':0.161,
        'sneeoosh':0.582,
        'kayakpoint':0.652,
        'nisqually':1.151,
        'tacoma':0.729,
        'seattle':0.865,
        'porttownsend':0.336,
        'cherrypoint':0.271}

Llat = {
        'bellingham':48+44.7/60,
        'sneeoosh':48+24.0/60,
        'kayakpoint':48+8.2/60,
        'nisqually':47.1183,
        'tacoma':47.2667,
        'seattle':47.6206,
        'porttownsend':48.1129,
        'cherrypoint':48+51.8/60}

Llon = {
        'bellingham':-122-29.7/60,
        'sneeoosh':-122-32.9/60,
        'kayakpoint':-122-22.0/60,
        'nisqually':-122.6650,
        'tacoma':-122.4133,
        'seattle':-122.3393,
        'porttownsend':-122.7595,
        'cherrypoint':-122-45.5/60}


pred_list = ['bellingham','sneeoosh','kayakpoint','nisqually']
obs_list = ['tacoma','seattle','porttownsend','cherrypoint']

def get_meta(mylist):
    sta_id = dict((k,Lsta_id[k]) for k in mylist)
    xtide_str = dict((k,Lxtide_str[k]) for k in mylist)
    mllw2navd88 = dict((k,Lmllw2navd88[k]) for k in mylist)
    lat = dict((k,Llat[k]) for k in mylist)
    lon = dict((k,Llon[k]) for k in mylist)
    return (mylist, sta_id, xtide_str,mllw2navd88,lat,lon)

def get_pred():
    return get_meta(pred_list)
    
def get_obs():
    return get_meta(obs_list)

def get_all():
    return get_meta(obs_list+pred_list)

def save_csv():
    (mylist, sta_id, xtide_str,mllw2navd88,lat,lon) = get_all()
    import pandas as pd
    df1 = pd.DataFrame.from_dict(sta_id,orient='index')
    df1 = df1.rename(index=str,columns={0:'noaaID'})
    df2 = pd.DataFrame.from_dict(lat,orient='index')
    df2 = df2.rename(index=str,columns={0:'lat'})
    df3 = pd.DataFrame.from_dict(lon,orient='index')
    df3 = df3.rename(index=str,columns={0:'lon'})
    df = pd.concat([df1,df2,df3],axis=1, join='outer')
    df.to_csv('../PointOutputs/tide_station_meta.csv')

    
if __name__ == "__main__":
    save_csv()
    





