#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 08:45:32 2020

@author: crosby
"""

import csv

csv_file = '/home/crosby/Documents/usgstidal/data-packager/datafolder/nisqually.bnd'

lat = []
lon = []
with open(csv_file) as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            lat.append(float(row[0]))
            lon.append(float(row[1]))
        except:
            print('Header')