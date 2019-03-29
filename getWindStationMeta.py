#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 12:47:06 2019

@author: crosby
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 15:57:11 2018

Retrieve location list for stations

@author: crosby
"""

# Full location info 
Lsta_id = {
        'tacomamet':'9446482',
        'porttownsend':'9444900',
        'cherrypoint':'9449424',
        'fridayharbor':'9449880',
        'neahbay':'9443090',
        'westport':'9441102',
        'tokepoint':'9440910',
        'portangeles':'9444090',
        'lapush':'9442396'}

Llat = {
        'tacomamet': 47+16.6/60,
        'porttownsend':48.1129,
        'cherrypoint':48+51.8/60,
        'fridayharbor':48+32.7/60,
        'neahbay':48+22.2/60,
        'westport':46+54.2/60,
        'tokepoint':46+42.5/60,
        'portangeles':48+7.5/60,
        'lapush':47+54.8/60}

Llon = {
        'tacomamet':-122-25.1/60,
        'porttownsend':-122.7595,
        'cherrypoint':-122-45.5/60,
        'fridayharbor':-123-0.8/60,
        'neahbay':-124-36.1/60,
        'westport':-124-6.3/60,
        'tokepoint':-123-58.0/60,
        'portangeles':-123-26.5/60,
        'lapush':-124-38.2/60}


full_list = ['tacomamet','porttownsend','cherrypoint','fridayharbor','neahbay','westport',
        'tokepoint','portangeles','lapush']

# Working set of sites
obs_list = ['tacomamet','porttownsend','cherrypoint','fridayharbor','westport',
        'tokepoint','portangeles','lapush']

def get_meta(mylist):
    sta_id = dict((k,Lsta_id[k]) for k in mylist)
    lat = dict((k,Llat[k]) for k in mylist)
    lon = dict((k,Llon[k]) for k in mylist)
    return (mylist, sta_id, lat,lon)
    
def get_obs():
    return get_meta(obs_list)

def save_csv():
    (mylist, sta_id,lat,lon) = get_obs()
    import pandas as pd
    df1 = pd.DataFrame.from_dict(sta_id,orient='index')
    df1 = df1.rename(index=str,columns={0:'noaaID'})
    df2 = pd.DataFrame.from_dict(lat,orient='index')
    df2 = df2.rename(index=str,columns={0:'lat'})
    df3 = pd.DataFrame.from_dict(lon,orient='index')
    df3 = df3.rename(index=str,columns={0:'lon'})
    df = pd.concat([df1,df2,df3],axis=1, join='outer')
    df.to_csv('../PointOutputs/wind_station_meta.csv')

    
if __name__ == "__main__":
    save_csv()
    





