# -*- coding: utf-8 -*-
"""
Download Tide Predictions for use in operational model

To find stations use this list: https://flaterco.com/xtide/locations.html
@author: Crosby S. C.
"""

import urllib2
import subprocess
import numpy as np
from datetime import datetime, timedelta
import time as timeP
import pickle
    
# Start and stop
start = datetime(2017,1,1)
stop = datetime(2023,1,1)

# Returns GMT offset to PST/PDT 
def get_gmt_offset_2():
    # Works through 2019, HARDCODED
    myTime = datetime.utcnow()
    if datetime(2015,3,8,2,0,0) < myTime < datetime(2015,11,1,2,0,0):
        GMT2PST = 7 #hr
    elif datetime(2016,3,13,2,0,0) < myTime < datetime(2016,11,6,2,0,0):
        GMT2PST = 7 #hr
    elif datetime(2017,3,12,2,0,0) < myTime < datetime(2017,11,5,2,0,0):
        GMT2PST = 7 #hr
    elif datetime(2018,3,11,2,0,0) < myTime < datetime(2018,11,4,2,0,0):
        GMT2PST = 7 #hr
    elif datetime(2019,3,10,2,0,0) < myTime < datetime(2019,11,3,2,0,0):
        GMT2PST = 7 #hr
    elif datetime(2020,3,8,2,0,0) < myTime < datetime(2020,11,1,2,0,0):
        GMT2PST = 7 #hr  
    elif datetime(2021,3,14,2,0,0) < myTime < datetime(2021,11,7,2,0,0):
        GMT2PST = 7 #hr        
    elif datetime(2022,3,13,2,0,0) < myTime < datetime(2022,11,6,2,0,0):
        GMT2PST = 7 #hr        
    else:
        GMT2PST = 8 #hr
    return GMT2PST

# Save location
save_loc = '../TidePredObs'
start_time = timeP.time()

# Locations 
sta_id = {
        'bellingham':'9449211',
        'sneeoosh':'9448576',
        'kayakpoint':'9448043',
        'nisqually':'9446828',
        'tacoma':'9446484',
        'seattle':'9447130',
        'porttownsend':'9444900'}

xtide_str = {
        'bellingham':'Bellingham, Bellingham Bay, Washington',
        'sneeoosh':'Sneeoosh Point, Washington',
        'kayakpoint':'Kayak Point, Washington',
        'nisqually':'Dupont Wharf, Nisqually Reach, Puget Sound, Washington',
        'tacoma':'Tacoma, Commencement Bay, Sitcum Waterway, Puget Sound, Washington',
        'seattle':'Seattle, Puget Sound, Washington',
        'porttownsend':'Port Townsend (Point Hudson), Admiralty Inlet, Washington'}

mllw2navd88 = {
        'bellingham':0.161,
        'sneeoosh':0.582,
        'kayakpoint':0.652,
        'nisqually':1.151,
        'tacoma':0.729,
        'seattle':0.865,
        'porttownsend':0.336}

method = 'xtide'


for loc in ['bellingham','sneeoosh','kayakpoint','nisqually','tacoma','seattle','porttownsend']:
    
    if method == 'xtide':
        # ------------------------- GET FROM XTIDE ---------------------------------
        # hour-by-hour tides
        command_str = 'tide -b \"{0:s}\" -e \"{1:s}\" -l \"{2:s}\" -z -mr -um -s 01:00'.\
            format( datetime.strftime(start,"%Y-%m-%d %H:%M"), datetime.strftime(stop,"%Y-%m-%d %H:%M"), xtide_str[loc] )
                
        tides_str = subprocess.check_output(command_str, shell=True)
        tide_raw = tides_str.split()
        Ntides = len(tide_raw) # combined number of dates and elevations
        
        tide = np.empty(Ntides/2, dtype='d')
        time_epoch = np.empty(Ntides/2, dtype='d')
        for tt in range(Ntides/2):
            time_epoch[tt] = tide_raw[2*tt]
            tide[tt] = tide_raw[2*tt-1]
        
        # Convert EPOCH time stamp to datetime
        time = [datetime.fromtimestamp(tt) for tt in time_epoch]
    
    elif method == 'noaa':
        #--------------------------GET FROM NOAA --------------------------------   
           
        # Build NOAA URLs     
        interval = 'h' # 'h' - hour, '6'- 6 minutes
        url1 = 'https://tidesandcurrents.noaa.gov/cgi-bin/predictiondownload.cgi?&stnid={:s}'.format(sta_id)
        url2 = '&threshold=&thresholdDirection=&bdate={:s}&edate={:s}&'.format(start.strftime('%Y%m%d'),stop.strftime('%Y%m%d'))
        url3 = 'units=metric&timezone=GMT&datum=MLLW&interval={:s}&clock=12hour&type=txt&annual=false'.format(interval)       
        url = url1 + url2 + url3
        
        # Download File to string
        aResp = urllib2.urlopen(url)
        web_pg = aResp.read()
        
        # Parse Data
        count = 0 
        tdate = []
        tide = []
        for m in web_pg.splitlines():
            count += 1
            if count > 14: # Skip header lines
                temp = m.split('\t')
                tdate.append(datetime.strptime(temp[0]+temp[2],'%Y/%m/%d%I:%M %p'))
                tide.append(float(temp[3]))
    
    else:
        raise ValueError('no method specificed')
    
    
    # Convert from MLLW to NAVD88
    tide = [tt-mllw2navd88[loc] for tt in tide]
    
    # Convert from Local to UTC
    pst2gmt = op_functions.get_gmt_offset_2()
    time = [tt+timedelta(hours=pst2gmt) for tt in time]
    
    # Save

    with open(save_loc + '/' + sta_id[loc] + '_pred_navd88.pkl','w') as f:
        pickle.dump([time,tide,sta_id[loc],mllw2navd88[loc],xtide_str[loc]],f)   
    
        
    ## Print data to file
    #with open('tide_pred_%s.txt' % sta_id,'w') as fid:
    #    fid.write('Date, Tide_NAVD88_Meters\n')
    #    for x,y in zip(time,tide):
    #        fid.write('%s %4.2f\n' % (x.strftime('%Y-%m-%d-%H-%M-%S'),y))
#    

print 'Total time elapsed: {0:.2f} minutes'.format(((timeP.time() - start_time)/60.))








## Quick plot
#plt.plot(tdate,tide)
#plt.plot(time,tide_xtide)
#plt.show()
#plt.close()

    
   
### Print data to file
#with open('tide_pred_%s_xtide.txt' % sta_id,'w') as fid:
#    fid.write('Date, Tide_NAVD88_Meters\n')
#    for x,y in zip(time,tide_xtide):
    


#---------------------OLD

## Set date start and end
#date_start = datetime.strptime('20170101','%Y%m%d')
#date_end = datetime.strptime('20211230','%Y%m%d')
#
## Build URL
#url_noaa = 'https://tidesandcurrents.noaa.gov/cgi-bin/predictiondownload.cgi?'
#url_sta = 'name=%s&state=WA&stnid=9448576&threshold=&thresholdDirection=&subordinate=false' % sta_str
#url_time = ('&referenceName=&referenceId=&heightOffsetLow=0.9&heightOffsetHigh=0.97&timeOffsetLow=39&timeOffsetHigh=32'+
#    '&heightAdjustedType=R&' + 'bdate={0:04d}{1:02d}{2:02d}'.format(date_start.year,date_start.month,date_start.day) +
#    '&edate={0:04d}{1:02d}{2:02d}'.format(date_end.year,date_end.month,date_end.day+1) + 
#    '&units=standard&timezone=GMT&datum=MLLW&interval=h&clock=12hour'+
#    '&type=txt&annual=false')
    