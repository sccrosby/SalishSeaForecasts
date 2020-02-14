#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:11:16 2019

@author: crosby
"""

import gzip
import shutil
import math
from datetime import datetime
import numpy as np
import scipy.io as io
import time as timer

# Set file structure
fol = '../ww3/latest'
cur_file = '{:s}/multi_1.46087.spec.gz'.format(fol)
out_fol = '../ww3/processed'
shared_loc = '/media/sf_VMShare'
transform_loc = shared_loc + '/SwellTransforms/Transforms_alongshore.mat'
save_loc = '../usgstidal/data-packager/datafolder'

# Reads floats from lines given, skips non-floats
def read_rows(lines,start,stop):
    var = []
    for ll in range(start,stop):
        temp = lines[ll].rstrip().split(' ')
        for t in temp:
            try:
                myfloat = float(t)
                var.append(myfloat)
            except:
                x = []
    return var

# Unzip to temp.txt
with gzip.open(cur_file,'rb') as f_in:
    with open('temp','wb') as f_out:
        shutil.copyfileobj(f_in,f_out)
       

startTime = timer.time()

# Read lines
fid = open('temp','r')
lines = fid.readlines()
fid.close()    

# Parse Freq and Dir in header
fr = read_rows(lines,1,8)
d = read_rows(lines,8,14)             

# Conert to np array
fr = np.array(fr)
d = np.array(d)

# Now grab data, 7 columns, 1800 per time step, 258 rows
Nd = len(d)
Nf = len(fr)
Ne = int(math.ceil(Nd*Nf/7.0))
Nt = 64

# Loop over data for each time step
rowI = 14 # Starting row for data
e3 = np.zeros((Nd,Nf,Nt))
time = []
tt = 0
while rowI < len(lines):
    # Grab time then move to data
    time.append(datetime.strptime(lines[rowI].rstrip(),'%Y%m%d %H%M%S'))
    rowI = rowI + 2
    e = read_rows(lines,rowI,rowI+Ne)
    rowI = rowI + Ne
    e2 = np.reshape(e,(Nd,Nf))
    e3[:,:,tt] = e2
    tt = tt + 1

# Convert to degrees
d = d*180/np.pi

# Convert to coming from
d = d + 180
d[d>360]=d[d>360]-360

# Reorder direction
I = np.argsort(d)
e3 = e3[I,:,:]
d = d[I]

# Create bandwidth
bw  = (0.5*(1.07-1./1.07))*fr

# Convert energy units to m^2/Hz/Deg
e3 = e3*np.pi/180

# Estimate wave height
ef = np.sum(e3,0)*10
hs = 4*np.sqrt(np.dot(ef.transpose(),bw))

# Load in tranforms
T = io.loadmat(transform_loc)

# Interpolate onto transforms axes
Nf2 = len(T['fr'][0])
Nd2 = len(T['dir'][0])


# First freq
e3i = np.empty((Nd,Nf2,Nt))
for tt in range(Nt):
    for dd in range(Nd):
        e3i[dd,:,tt] = np.interp(T['fr'][0],fr,e3[dd,:,tt])

# Second direction
e3ii = np.empty((Nd2,Nf2,Nt))
for tt in range(Nt):
    for ff in range(Nf2):
        e3ii[:,ff,tt] = np.interp(T['dir'][0],d,e3i[:,ff,tt])

# Transform
lat = T['lat']
lon = T['lon']
lat_bounds = [min(lat), max(lat)]
lon_bounds = [min(lon), max(lon)]
A_bw = T['bw'][0] 
        
A_hs = np.empty((len(lat),Nt))
A_Tp = np.empty((len(lat),Nt))
A_dir = np.empty((len(lat),Nt)) # In development, placeholder for now
for tt in range(Nt):
    for xx in range(len(lat)):
        temp = np.multiply(T['T_e'][:,:,xx],e3ii[:,:,tt])
        tempef = np.sum(temp,0)*10
        I = np.argmax(tempef)
        A_Tp[xx,tt] = 1./T['fr'][0][I]
        A_hs[xx,tt] = 4*np.sqrt(np.dot(tempef.transpose(),A_bw))                    
        

# Save
io.savemat('{:s}/jdf_swell.mat'.format(save_loc),{'hs':A_hs,'dp':A_dir,'tm':A_Tp,
'lat':lat,'lon':lon,'lat_limits':lat_bounds,'lon_limits':lon_bounds})    

    
print 'Total time elapsed: {0:.2f} minutes'.format(((timer.time() - startTime)/60.))
        

# Save mat file out for error checking
# io.savemat('{:s}/Buoy46087spec.mat'.format(out_fol),{'e':e3,'fr':fr,'dir':d})



#
#import matplotlib.pyplot as plt
#plt.subplot(121)
#plt.pcolor(fr,d,e3[:,:,10])
#plt.ylabel('Dir')
#plt.xlabel('Fr')
#plt.xlim((0.05,.2))
#plt.ylim((180,360))
#
#
#plt.subplot(122)
#plt.pcolor(T['fr'][0],T['dir'][0],e3ii[:,:,10])
#plt.ylabel('Dir')
#plt.xlabel('Fr')
#plt.colorbar()
#
#










