import requests
import numpy as np
import datetime as dt
import pytz
from dateutil import parser

def get_coops_data(station,
                   start_date,
                   end_date,
                   product='hourly_height',
                   units='metric',
                   datum='MLLW',
                   time_zone='GMT',
                   interval=False):
    """
    units can be 'english' or 'metric'

    start_date and end_date must be formatted like:
    yyyyMMdd, yyyyMMdd HH:mm, MM/dd/yyyy, or MM/dd/yyyy HH:mm

    product options include 'water_level', 'hourly_height', 'predictions'
    from https://tidesandcurrents.noaa.gov/api/
    Option	Description
    water_level	Preliminary or verified water levels, depending on availability.
    air_temperature	Air temperature as measured at the station.
    water_temperature	Water temperature as measured at the station.
    wind	Wind speed, direction, and gusts as measured at the station.
    air_pressure	Barometric pressure as measured at the station.
    air_gap	Air Gap (distance between a bridge and the water's surface) at the station.
    conductivity	The water's conductivity as measured at the station.
    visibility	Visibility from the station's visibility sensor. A measure of atmospheric clarity.
    humidity	Relative humidity as measured at the station.
    salinity	Salinity and specific gravity data for the station.
    hourly_height	Verified hourly height water level data for the station.
    high_low	Verified high/low water level data for the station.
    daily_mean	Verified daily mean water level data for the station.
    monthly_mean	Verified monthly mean water level data for the station.
    one_minute_water_level	One minute water level data for the station.
    predictions	6 minute predictions water level data for the station.
    datums	datums data for the stations.
    currents	Currents data for currents stations.
    """

    url = 'http://tidesandcurrents.noaa.gov/api/datagetter?product=' \
    + product \
    + '&application=NOS.COOPS.TAC.WL&begin_date=' \
    + str(start_date) \
    + '&end_date=' \
    + str(end_date) \
    + '&datum=' \
    + datum \
    + '&station=' \
    + str(station) \
    + '&time_zone=' \
    + time_zone \
    + '&units=' \
    + units \
    + '&format=json'

    if interval:
        url = url + '&interval=' + interval

    payload = requests.get(url).json()

    if 'error' in payload.keys():
        raise ValueError('Error in returning dataset: ' + payload['error']['message'])


    if product == 'water_level' or product == 'hourly_height' or product == 'wind':
        d = payload['data']
    elif product == 'predictions':
        d = payload['predictions']
    elif product == 'wind':
        d = payload(['data'])
 


    #'d', direction, 'g' - gust, 'f' ?, s - 'speed'
    if product == 'wind':
        t = []
        a = []
        g = []
        f = []
        s = []
        for n in range(len(d)):
            t.append(pytz.utc.localize(parser.parse(d[n]['t'])))
            try:
                a.append(float(d[n]['d']))
            except:
                a.append(np.nan)  
            try:
                g.append(float(d[n]['g']))
            except:
                g.append(np.nan)     
            try:
                f.append(float(d[n]['f']))
            except:
                f.append(np.nan)     
            try:
                s.append(float(d[n]['s']))
            except:
                s.append(np.nan)     
                
        n = {}
        n['time'] = np.array(t)
        n['d'] = np.array(a)
        n['g'] = np.array(g)
        n['f'] = np.array(f)
        n['s'] = np.array(s)
                
                
    
    else:
        t = []
        v = []
        for n in range(len(d)):
            t.append(pytz.utc.localize(parser.parse(d[n]['t'])))
            try:
                v.append(float(d[n]['v']))
            except:
                v.append(np.nan)
    
        n = {}
        n['time'] = np.array(t)
        n['v'] = np.array(v)

    return n
