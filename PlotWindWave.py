#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 10:39:48 2018
Create wind and wave plots

@author: crosby
"""

# Needed for use with crontab, By default matplotlib uses x-windows, see https://stackoverflow.com/questions/2801882/generating-a-png-with-matplotlib-when-display-is-undefined
# To test crontab in its environment, use: env -i sh -c './run_script.sh'
import matplotlib
matplotlib.use('Agg')

import argparse
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
import time

# Set up color constants
colors = [[0.007843137254902,  0.074509803921569,  0.670588235294118],
            [                0,                  0,  1.000000000000000],
            [                0,  0.534883720930233,  1.000000000000000],
            [                0,  1.000000000000000,  0.906976744186047],
            [                0,  1.000000000000000,  0.162790697674419],
            [1.000000000000000,  1.000000000000000,                  0],
            [1.000000000000000,  0.441860465116279,                  0],
            [1.000000000000000,                  0,  0.116279069767442],
            [0.670588235294118,                  0,                  0],
            [1.000000000000000,                  0,  0.860465116279070],
            [0.558139534883721,                  0,  0.558139534883721],
            [0.023255813953488,                  0,  0.023255813953488]]
color_map = LinearSegmentedColormap.from_list("mycolors", colors)


def wave_height_plot(W, T, saveName):
    for fh in range(48):
        wave_contours = [i/2. for i in range(0,13)]
        wave_ticks    = [i/2. + 0.25 for i in range(0,12)]
    
        min_x, max_x = T['xim'][0,0], T['xim'][0,-1]
        min_y, max_y = T['yim'][0,-1], T['yim'][0,0]
        bounds = [min_x, max_x, max_y, min_y]    
    
        plt.figure(figsize=(5,5))
        plt.imshow(T['im'], extent=bounds, origin='lower')
        plt.xlim(W['lon_limits'][0])
        plt.ylim(W['lat_limits'][0])
         
        im = plt.contourf(W['lon'], W['lat'], W['hs'][:,:,fh]*3.28, wave_contours, cmap=color_map, vmin=min(wave_contours), vmax=max(wave_contours))
        
        cb = plt.gcf().colorbar(im, ticks=wave_ticks, fraction=0.05, pad=0.05)
        cb.ax.set_yticklabels(wave_contours[1:])
        cb.set_label('Hs [ft]')
    
        thin = 15
        wave_dir = 90 - W['dp'][:,:,fh] + 180
        wave_X = W['lon'][::thin,::thin]
        wave_Y = W['lat'][::thin,::thin]
        wave_U = np.cos(np.deg2rad(wave_dir[::thin,::thin]))
        wave_V = np.sin(np.deg2rad(wave_dir[::thin,::thin]))
        plt.quiver(wave_X, wave_Y, wave_U, wave_V, scale=22.0)
    
        plt.savefig('../Plots/{:s}_Hs{:02d}.png'.format(saveName,fh),dpi=200)
        plt.close()

def wind_plot(W, T):
    wind_contours = [5*i for i in range(13)]
    wind_ticks = [2.5 + 5*i for i in range(12)]

    min_x, max_x = T['xim'][0,0], T['xim'][0,-1]
    min_y, max_y = T['yim'][0,-1], T['yim'][0,0]
    bounds = [min_x, max_x, max_y, min_y]

    plt.imshow(T['im'], extent=bounds, origin='lower')
    plt.xlim([-123.2, -122.2])
    plt.ylim([47, 48.1])

    wind_speed = np.sqrt(W['Windv_x']**2 + W['Windv_y']**2)
    wind_speed[wind_speed == 0] = np.nan
    
    im = plt.contourf(W['Xp'], W['Yp'], wind_speed*2.23694, wind_contours, cmap=color_map, vmin=min(wind_contours), vmax=max(wind_contours))

    cb = plt.gcf().colorbar(im, fraction=0.05, pad=0.05)
    cb.set_label('Wind Speed [mph]')

    thin = 15
    wind_X = W['Xp'][::thin,::thin]
    wind_Y = W['Yp'][::thin,::thin]
    wind_U = W['Windv_x'][::thin,::thin]
    wind_V = W['Windv_y'][::thin,::thin]
    plt.quiver(wind_X, wind_Y, wind_U, wind_V)

    plt.show()


def main():
    parser = argparse.ArgumentParser('swan_plots.py')
    parser.add_argument('--model-output', type=str, required=True,
            help='Output of SWAN model run (.mat format)')
    parser.add_argument('--basemap', type=str, required=True,
            help='Imagery for basemap (.mat format)')
    parser.add_argument('--wave-plot', action='store_true',
            help='Generate a wave height plot')
    parser.add_argument('--wind-plot', action='store_true',
            help='Generate a wind speed plot')
    args = parser.parse_args()

    if not os.path.exists(args.model_output):
        print('File not found: %s' % args.model_output)
        exit(1)
    if not os.path.exists(args.basemap):
        print('File not found: %s' % args.basemap)
        exit(1)

    W = scipy.io.loadmat('Spatial.mat') 
    T = scipy.io.loadmat('PugetSound150.mat')

    if args.wave_plot:
        wave_height_plot(W, T)
    if args.wind_plot:
        wind_plot(W, T)


if __name__ == "__main__":       

    startTime = time.time()

    #--------------------------------Bellingham------------------------------#    
    # Choose Model and determine locations
    shared_loc = '/media/sf_VMShare'
    saveName = 'BellinghamBay'
    wave_loc = '../LUToutputs/bellingham.mat'
    imagery_loc = shared_loc + '/Imagery/BellinghamBayImagery.mat'

    # Load in appropriate forecasts and imagery
    W = scipy.io.loadmat(wave_loc) 
    T = scipy.io.loadmat(imagery_loc)    
    
    # Generate 48 Hs plots for each forecast hour 
    wave_height_plot(W, T, saveName)
    #------------------------------------------------------------------------#

    #--------------------------------Skagit------------------------------#    
    # Choose Model and determine locations
    shared_loc = '/media/sf_VMShare'
    saveName = 'SkagitDelta'
    wave_loc = '../LUToutputs/skagit.mat'
    imagery_loc = shared_loc + '/Imagery/SkagitImagery.mat'

    # Load in appropriate forecasts and imagery
    W = scipy.io.loadmat(wave_loc) 
    T = scipy.io.loadmat(imagery_loc)    
    
    # Generate 48 Hs plots for each forecast hour 
    wave_height_plot(W, T, saveName)
    #------------------------------------------------------------------------#
    
    print 'Total time elapsed: {0:.2f} minutes'.format(((time.time() - startTime)/60.))
    
  
    
    
    
    
    
    
    
    
    
    
    
