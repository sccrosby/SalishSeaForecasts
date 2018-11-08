#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 16:03:11 2018

@author: crosby
"""
from scipy import io

fol_input = '../gdps/PostProcessed'
fol_output = '../PointOutputs'

pt_name = ['BellinghamBay','SkagitDelta','PortSusan']
pt_lon = [-122.565234, -122.512193, -122.413508]
pt_lat = [48.715758, 48.338880, 48.172197]



# Load predictions of slp
nn = 1
outfile = '{0:s}/{1:s}_slp'.format(fol_output,pt_name[nn])
gdps = io.loadmat(outfile)

# Load tide predictions


# Load tide observations?


# Load wave predictions? 
