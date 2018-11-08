#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 14:12:38 2018

Upload plots to wwu 

@author: crosby
"""

import pysftp

# Location credentials
ftp_server = 'webtechlamp2.eis.wwu.edu'
user = 'crosbys4'
pwd = 'Md7!5r2v90'

# Select Directory with files to move (moves all files) and destination on server
dest = 'WavePlots'
loc = '../Plots'

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with pysftp.Connection(host=ftp_server,username=user,password=pwd, cnopts=cnopts) as srv:
    srv.put_d(loc,dest,preserve_mtime=True)

srv.close()


