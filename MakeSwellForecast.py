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

# Set file structure
fol = '../ww3/latest'
cur_file = '{:s}/multi_1.46087.spec.gz'.format(fol)
out_fol = '../ww3/processed'

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
       

# Read lines
fid = open('temp','r')
lines = fid.readlines()
fid.close()    

# Parse Freq and Dir in header
fr = read_rows(lines,1,8)
d = read_rows(lines,8,14)             

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

# Save mat file out for error checking
io.savemat('{:s}/Buoy46087spec.mat'.format(out_fol),{'e':e3,'fr':fr,'dir':d})



import matplotlib.pyplot as plt
plt.pcolor(e3[:,:,-1])















