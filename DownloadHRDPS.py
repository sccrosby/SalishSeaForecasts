#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Functions download the latest HRDPS forecast
Created on Thu Sep 20 10:10:16 2018
@author: s. c. crosby
"""

import os
import time
import urllib2
import pickle
from datetime import datetime, timedelta

# Locations to save HRDPS
fol_hrdps = '../hrdps'

# Static HRDPS information
hrdps_PrefixP           = 'CMC_hrdps_west_PRMSL_MSL_0_rotated_latlon0.009x0.009_' 
hrdps_PrefixU           = 'CMC_hrdps_west_UGRD_TGL_10_rotated_latlon0.009x0.009_'
hrdps_PrefixV           = 'CMC_hrdps_west_VGRD_TGL_10_rotated_latlon0.009x0.009_'
hrdps_PrefixLAND        = 'CMC_hrdps_west_LAND_SFC_0_rotated_latlon0.009x0.009_'
hrdps_url               = 'http://dd.alpha.weather.gc.ca/model_hrdps/west/1km/grib2'
hrdps_lamwest_file      = '../hrdps/lamwestpoints.dat'
hrdps_rotation_file     = '../hrdps/rotations.dat'
num_forecast_hours      = 36

#Primary function called, downloads latest forecast from HRDPS 
def get_hrdps(date_string, zulu_hour):    
		
		# Set folder for downloads
		loc_output = '{0:s}/{1:s}'.format(fol_hrdps,date_string)
   
		# Make output folder if neccessary
		if os.path.exists(loc_output):
				temp=0 #Do nothing
		else:
				os.mkdir(loc_output)
		
		# Dowload land mask? !!!LAND DOESN'T EXIST!!!
		#download_grib(hrdps_PrefixLAND, hrdps_url, date_string, zulu_hour, 0, loc_output)
				 
		# Download grib files
		for hour in range(num_forecast_hours): 
				print 'Dowloading hrdps forecast hour %02d' % hour
				# Pressure (prtmsl)    
				download_grib(hrdps_PrefixP, hrdps_url, date_string, zulu_hour, hour, loc_output)      
				# U wind    
				download_grib(hrdps_PrefixU, hrdps_url, date_string, zulu_hour, hour, loc_output)       
				# V wind    
				download_grib(hrdps_PrefixV, hrdps_url, date_string, zulu_hour, hour, loc_output)
 

def download_grib(gribPrefixP, url, dateString, zulu_hour, forecast_hour, loc_output):
		# Set name and creat URL
		grib_name = '%s%sT%02dZ_P%03d-00.grib2' % (gribPrefixP, dateString, zulu_hour, forecast_hour)
		grib_url = '%s/%02d/%03d/%s' % (url, zulu_hour, forecast_hour, grib_name)
		print(grib_url)
	
		# Download file to folder specified, throw error if not found
		outfile = '%s/%s' % (loc_output,grib_name)
		try:
				webpage = urllib2.urlopen(grib_url)
				with open(outfile,'w') as fid:
						temp = webpage.read()
						fid.write(temp)
		except:
				print 'First download attempt failed, trying 10 more times'       
				for i in range(1):        
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

def latest_hrdps_forecast():
	
		# Set static string and format
		gribPrefix = 'CMC_hrdps_west_PRMSL_MSL_0_rotated_latlon0.009x0.009_' #full url example https://dd.alpha.weather.gc.ca/model_hrdps/west/1km/grib2/12/000/CMC_hrdps_west_PRMSL_MSL_0_rotated_latlon0.009x0.009_20200714T12Z_P000-00.grib2
		forecastHr = 36
		
		for ndy in [0,-1]:
						 NowUTC = datetime.utcnow() + timedelta(days=ndy)
						 dateString = NowUTC.strftime('%Y%m%d')
				
						 # Try most recent forecast first, then go backwards
						 for runStart in [12,0]:
									gribName = '{0:s}{1:s}T{2:02d}Z_P{3:03d}-00.grib2'.format(gribPrefix, dateString, runStart, forecastHr)
									gribUrl   = 'http://dd.alpha.weather.gc.ca/model_hrdps/west/1km/grib2/{0:02d}/{1:03d}/{2:s}'.format(runStart, forecastHr, gribName)
									print(gribUrl)
						
									# See if file exists, if so return, otherwise loop
									try:
												  urllib2.urlopen(gribUrl)
												  forecastHour = runStart
												  print('Found most recent file {0:s}, {1:02d}Z\n'.format(dateString, runStart)),
												  return dateString, forecastHour
									except:
												  print('48 hour file doesn\'t exist yet for {0:s}, {1:02d}Z\n'.format(dateString, runStart)),

		#If no files found return null
		dateString = 'null'
		forecastHour = 0
		return dateString, forecastHour




def main():


		(date_string, zulu_hour) = latest_hrdps_forecast()
		print(date_string)
		print(zulu_hour)
		
		test_file = '{0:s}/{1:s}/{2:s}{1:s}{3:02d}_P047-00.grib2'.format(fol_hrdps,date_string,hrdps_PrefixP,zulu_hour)
		print(test_file)
		if os.path.isfile(test_file):
				print 'Grib files already downloaded, skipping'
		else:
				get_hrdps(date_string, zulu_hour)
				
		# Save current time step
		with open('current_forecast.pkl','w') as f:
				pickle.dump([date_string, zulu_hour],f)

		
if __name__ == "__main__":
		main()
