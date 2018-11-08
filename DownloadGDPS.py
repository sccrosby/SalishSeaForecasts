#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Functions download the latest GDPS forecast
Created on Thu Sep 20 10:10:16 2018
@author: s. c. crosby
https://weather.gc.ca/grib/grib2_glb_25km_e.html
"""

import os
import time
import urllib2
import pickle
from datetime import datetime, timedelta

# Locations to save GDPS
fol_gdps = 'gdps'

# Static GDPS information 
#   CMC_glb_PRMSL_MSL_0_latlon.24x.24_2018103100_P000.grib2  
#   CMC_glb_PRMSL_MSL_0_latlon.24x.24_2018103100_P003.grib2    
gdps_PrefixP           = 'CMC_glb_PRMSL_MSL_0_latlon.24x.24_' 
gdps_PrefixU           = 'CMC_glb_UGRD_TGL_10_latlon.24x.24_'
gdps_PrefixV           = 'CMC_glb_VGRD_TGL_10_latlon.24x.24_'
gdps_PrefixLAND        = 'CMC_glb_LAND_SFC_0_latlon.24x.24_'
gdps_url               = 'http://dd.weather.gc.ca/model_gem_global/25km/grib2/lat_lon/'

forecast_hours =  range(0,243,3)
num_forecast_hour = len(forecast_hours)

#Primary function called, downloads latest forecast from GDPS 
def get_gdps(date_string, zulu_hour):    
    
    # Set folder for downloads
    loc_output = '../{0:s}/{1:s}'.format(fol_gdps,date_string)
   
    # Make output folder if neccessary
    if os.path.exists(loc_output):
        temp=0 #Do nothing
    else:
        os.mkdir(loc_output)
    
    # Dowload land mask?
    download_grib(gdps_PrefixLAND, gdps_url, date_string, zulu_hour, 0, loc_output)
         
    # Download grib files
    for hour in forecast_hours: 
        print 'Dowloading gdps forecast hour %02d' % hour
        # Pressure (prtmsl)    
        download_grib(gdps_PrefixP, gdps_url, date_string, zulu_hour, hour, loc_output)      
        # U wind    
        #download_grib(gdps_PrefixU, gdps_url, date_string, zulu_hour, hour, loc_output)       
        # V wind    
        #download_grib(gdps_PrefixV, gdps_url, date_string, zulu_hour, hour, loc_output)  

 

def download_grib(gribPrefixP, url, dateString, zulu_hour, forecast_hour, loc_output):
    # Set name and creat URL
# CMC: constant string indicating that the data is from the Canadian Meteorological Centre
# glb: constant string indicating that the data is from the GDPS
# Variable: Variable type included in this file. To consult a complete list, refer to the Data in GRIB2 format section.
# LevelType: Level type. To consult a complete list, refer to the Data in GRIB2 format section.
# Level: Level value. To consult a complete list, refer to the Data in GRIB2 format section.
# Projection: projection used for the data. Can take the values [latlon, ps]
# YYYYMMDD: Year, month and day of the beginning of the forecast.
# HH: UTC run time [00, 12]
# Phhh: P is a constant character. hhh is the forecast hour [000, 003, 006, ..., 240]
# grib2: constant string indicating the GRIB2 format is used

# example gribfile name: CMC_glb_PRMSL_MSL_0_latlon.24x.24_2018101500_P000.grib2  

    grib_name = '{:s}{:s}{:02d}_P{:03d}.grib2'.format(gribPrefixP, dateString, zulu_hour, forecast_hour)
    grib_url = '{:s}/{:02d}/{:03d}/{:s}'.format(url, zulu_hour, forecast_hour, grib_name)

    # Download file to folder specified
    outfile = '%s/%s' % (loc_output,grib_name)
    try:
        webpage = urllib2.urlopen(grib_url)
        with open(outfile,'w') as fid:
            temp = webpage.read()
            fid.write(temp)
    except:
        print 'First download attempt failed, trying 10 more times'       
        for i in range(10):        
            time.sleep(1)        
            try:
                webpage = urllib2.urlopen(grib_url)
                with open(outfile,'w') as fid:
                    temp = webpage.read()
                    fid.write(temp)
                msg = 'working'
                print 'Attempt {:d} {:s}'.format(i,msg)
                break
            except:
                msg = 'failed'
                print 'Attempt {:d} {:s}'.format(i,msg)
                
        if msg == 'failed':
            err_str = 'Grib file not found, url is incorrect. Check url, {:s}'.format(grib_url)    
            with open('Errfile.txt','w') as f:
                f.write(err_str)            
            raise ValueError(err_str)

def latest_gdps_forecast():
	# Set static string and format
    forecast_hour = 240
	
    # Try today and yesterday
    for ndy in [0,-1]:
        NowUTC = datetime.utcnow() + timedelta(days=ndy)
        dateString = NowUTC.strftime('%Y%m%d')
		
		# Try most recent forecast first, then go backwards
        for zulu_hour in [12,0]:
            grib_name = '{:s}{:s}{:02d}_P{:03d}.grib2'.format(gdps_PrefixP, dateString, zulu_hour, forecast_hour)
            grib_url = '{:s}/{:02d}/{:03d}/{:s}'.format(gdps_url, zulu_hour, forecast_hour, grib_name)
            print(grib_url)
            
            # See if file exists, if so return, otherwise loop
            try:
            	   urllib2.urlopen(grib_url)
            	   return dateString, zulu_hour
            except:
                print('Forecast hour file doesn\'t exist yet for {0:s}, {1:02d}Z\n'.format(dateString, zulu_hour)),

    #If no files found return null
    dateString = 'null'
    zulu_hour = 'null'
    return dateString, zulu_hour


def main():
    (date_string, zulu_hour) = latest_gdps_forecast()
        
    # Test file
    forecast_hour= 240
    grib_name = '{:s}{:s}{:02d}_P{:03d}.grib2'.format(gdps_PrefixP, date_string, zulu_hour, forecast_hour)
    test_file = '../{0:s}/{1:s}/{2:s}'.format(fol_gdps,date_string,grib_name)

    if os.path.isfile(test_file):
        print 'GDPS grib files already downloaded'
    else:
        get_gdps(date_string, zulu_hour)
        
    # Save current time step
    with open('current_forecast_gdps.pkl','w') as f:
        pickle.dump([date_string, zulu_hour],f)
    
if __name__ == "__main__":
    main()
