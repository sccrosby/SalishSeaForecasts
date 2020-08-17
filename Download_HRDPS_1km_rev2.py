#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, ssl
import time
import urllib
import shutil
#import urllib
import pickle
#import ssl
from datetime import datetime, timedelta

# Run this to avoid security issue in downloading from unsecure HTTP
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# Locations to save GDPS
fol_hrdps1 = 'hrdps1km'

# Static GDPS information
#   CMC_glb_PRMSL_MSL_0_latlon.24x.24_2018103100_P000.grib2
#   CMC_glb_PRMSL_MSL_0_latlon.24x.24_2018103100_P003.grib2
gdps_PrefixP           = 'CMC_hrdps_west_PRMSL_MSL_0_rotated_latlon0.009x0.009_'
gdps_PrefixU           = 'CMC_hrdps_west_UGRD_TGL_10_rotated_latlon0.009x0.009_'
gdps_PrefixV           = 'CMC_hrdps_west_VGRD_TGL_10_rotated_latlon0.009x0.009_'
gdps_PrefixLAND        = 'CMC_hrdps_west_LAND_SFC_0_rotated_latlon0.009x0.009_'
gdps_url               = 'https://dd.alpha.weather.gc.ca/model_hrdps/west/1km/grib2'

forecast_hours =  range(0,36,1)
num_forecast_hour = len(forecast_hours)


# In[2]:


def get_hrdps1(date_string, zulu_hour):

    # Set folder for downloads
    loc_output = '../{0:s}/{1:s}'.format(fol_hrdps1,date_string)

    # Make output folder if neccessary
    if os.path.exists(loc_output):
        temp=0 #Do nothing
    else:
        os.mkdir(loc_output)

    # Download grib files
    for hour in forecast_hours:
        print('Dowloading gdps forecast hour{:02d}',hour)
        # Pressure (prtmsl)
        download_grib(gdps_PrefixP, gdps_url, date_string, zulu_hour, hour, loc_output)
        # U wind
        download_grib(gdps_PrefixU, gdps_url, date_string, zulu_hour, hour, loc_output)
        # V wind
        download_grib(gdps_PrefixV, gdps_url, date_string, zulu_hour, hour, loc_output)


# In[3]:


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

    grib_name = '{:s}{:s}T{:02d}Z_P{:03d}-00.grib2'.format(gdps_PrefixP, dateString, zulu_hour, forecast_hour)
    grib_url = '{:s}/{:02d}/{:03d}/{:s}'.format(gdps_url, zulu_hour, forecast_hour, grib_name)
    #print(grib_url)

    # Download file to folder specified
    outfile = '%s/%s' % (loc_output,grib_name)
    try:
        response = urllib.request.urlretrieve(grib_url,outfile)
    except:
        print('First download attempt failed, trying 10 more times')
        for i in range(10):
            time.sleep(1)
            try:
                response = urllib.request.urlopen(grib_url)
                with open(outfile, 'wb') as fname:
                    shutil.copyfileobj(response, fname)
                print('Attempt {:d} {:s}',i,msg)
                break
            except:
                msg = 'failed'
                print('Attempt {:d} {:s}',i,msg)

        if msg == 'failed':
            err_str = 'Grib file not found, url is incorrect. Check url, {:s}'.format(grib_url)
            with open('Errfile.txt','w') as f:
                f.write(err_str)
            raise ValueError(err_str)


# In[4]:


def latest_hrdps_forecast():
	# Set static string and format
    forecast_hour = 36

    # Try today and yesterday
    for ndy in [0,-1]:
        NowUTC = datetime.utcnow() + timedelta(days=ndy)
        dateString = NowUTC.strftime('%Y%m%d')

		# Try most recent forecast first, then go backwards
        for zulu_hour in [12,0]:
            grib_name = '{:s}{:s}T{:02d}Z_P{:03d}-00.grib2'.format(gdps_PrefixP, dateString, zulu_hour, forecast_hour)
            grib_url = '{:s}/{:02d}/{:03d}/{:s}'.format(gdps_url, zulu_hour, forecast_hour, grib_name)
            print(grib_url)

            # See if file exists, if so return, otherwise loop
            try:
                response = urllib.request.urlopen(grib_url)
                return dateString, zulu_hour
            except:
                print('Forecast hour file doesn\'t exist yet for {0:s}, {1:02d}Z\n'.format(dateString, zulu_hour)),

    #If no files found return null
    dateString = 'null'
    zulu_hour = 'null'
    return dateString, zulu_hour


# In[ ]:


(date_string, zulu_hour) = latest_hrdps_forecast()
print(date_string)
print(zulu_hour)

# Test file
forecast_hour= 36
grib_name = '{:s}{:s}T{:02d}Z_P{:03d}-00.grib2'.format(gdps_PrefixP, date_string, zulu_hour, forecast_hour)
test_file = '../{0:s}/{1:s}/{2:s}'.format(fol_hrdps1,date_string,grib_name)

if os.path.isfile(test_file):
    print('HRDPS-Experimental grib files already downloaded')
else:
    get_hrdps1(date_string, zulu_hour)

# Save current time step
with open('current_forecast_hrdps1km.pkl','w') as f:
    pickle.dump([date_string, zulu_hour],f)


# In[ ]:




