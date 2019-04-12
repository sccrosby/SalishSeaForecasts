#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:57:22 2019
Data source, NOAA, ftp://polar.ncep.noaa.gov/pub/waves/develop
@author: crosby
"""

from datetime import datetime,timedelta
import math
from ftplib import FTP

# Output Folder
out_latest = '../ww3/latest'

def grabFile(ftp_fol,ftp_file,out_fol):

    localfile = open(out_fol+'/'+ftp_file, 'wb')
    ftp.retrbinary('RETR ' + ftp_fol+ftp_file, localfile.write, 1024)

    ftp.quit()
    localfile.close()

# Download WW3 Spectra Forecasts at Buoy site
noaa_id = '46087' # Neah Bay

# Create Locations and current time
hours_back = 12 # Give time for WW3 forecast to run/post
nowUTC = datetime.utcnow()-timedelta(hours=hours_back)
dateString = nowUTC.strftime('%Y%m%d')
zulu_hour = int(math.floor((nowUTC.hour)/6.0)*6)

ftp_src = 'polar.ncep.noaa.gov'
ftp_fol = '/pub/waves/develop/multi_1.{:s}.t{:02d}z/'.format(dateString,zulu_hour)
ftp_file = 'multi_1.{:s}.spec.gz'.format(noaa_id)

# Connect to FTP and download
link = ftp_fol+ftp_file
ftp = FTP(ftp_src)
ftp.login()
grabFile(ftp_fol,ftp_file,out_latest)

print 'Downloaded WW3 Spectra at Neah from {:s}, hour {:d}'.format(dateString,zulu_hour)



