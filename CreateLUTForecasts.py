#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 12:52:24 2018

Use LUTinputs and LUT results to construct a forecast

To install pkml, pip install pykml

@author: s. c. crosby
"""

from pykml import parser 
from scipy import io
from scipy.interpolate import griddata 

from matplotlib import path
import pickle
import numpy as np
import math
from datetime import datetime
import time
import csv
import getwaveLUTmeta

save_loc = '../usgstidal/data-packager/datafolder'

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def get_bounds(mask,lat,lon):
    (Nx,Ny) = mask.shape
    test = 0
    row_l = -1
    while test == 0:
        row_l = row_l + 1
        test = max(mask[row_l,:])
                
    test = 0
    row_u = Nx
    while test == 0:
        row_u = row_u - 1
        test = max(mask[row_u,:])

    test = 0
    col_l = -1
    while test == 0:
        col_l = col_l + 1
        test = max(mask[:,col_l])
                
    test = 0
    col_u = Ny
    while test == 0:
        col_u = col_u - 1
        test = max(mask[:,col_u])
        
    return (row_l,row_u,col_l,col_u)

def regrid(x,y,z,x2,y2):
    ind = np.isnan(x)   
    x = x[~ind]
    y = y[~ind]
    z = z[~ind]
    z2 = griddata((x, y), z, (x2,y2), method='linear' )
    return z2

def read_kml(kml_file):
    root = parser.fromstring(open(kml_file,'r').read())
    coord = str(root.Document.Placemark.LineString.coordinates)
    coord = coord.strip('\n')
    coord = coord.strip('\t')
    coord = coord.strip('\n')
    coord = coord.split(',')
    
    lon = coord[0::2]
    lat = coord[1::2]
    
    lon.pop(-1)
    
    lon[0] = float(lon[0])
    lon[1:] = [float(x[2:]) for x in lon[1:]]
    lat = [float(x) for x in lat]
    return (lat,lon)

def read_bnd(bnd_file):
    lat = []
    lon = []
    with open(bnd_file) as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                lat.append(float(row[0]))
                lon.append(float(row[1]))
            except:
                print('Header')    
    return (lat,lon)

def load_jdf_lut(u,d,t,Nx,Ny,lut_loc,lut_prefix):
    if u == 0:
        lut = {};
        lut['Hsig'] = np.zeros((Nx,Ny))
        lut['Dir'] = np.zeros((Nx,Ny))
        lut['Tm01'] = np.zeros((Nx,Ny))
        
    elif d == 360:
        d = 0
        fname_lut = '{:s}_s{:d}_d{:d}_t{:d}.mat'.format(lut_prefix,int(u*10),int(d),int(t*10))
        lut = io.loadmat(lut_loc+'/'+fname_lut,squeeze_me=True,variable_names=['Hsig','Dir','Tm01'])   
    else:
        fname_lut = '{:s}_s{:d}_d{:d}_t{:d}.mat'.format(lut_prefix,int(u*10),int(d),int(t*10))
        lut = io.loadmat(lut_loc+'/'+fname_lut,squeeze_me=True,variable_names=['Hsig','Dir','Tm01'])     
    return lut

def save_lut_forecast(model_name,hrdps_loc,tide_loc,shared_loc,lut_loc,bnd_file,lut_prefix,date_string,zulu_hour):
    # Load kml mask
    (lat,lon) = read_bnd(bnd_file)
    
    # read in hrdps
    hrdps = io.loadmat(hrdps_loc)
    
    # Read in tide
    tide = pickle.load(open(tide_loc,'rb'))   
    
    # Forecast time
    temp = '%s%02d' % (date_string, zulu_hour)
    time_forecast =  datetime.strptime(temp,'%Y%m%d%H')
    
    # Find tide indice
    time_nearest = nearest(tide[0],time_forecast)
    idx = tide[0].index(time_nearest)
    tide_forecast = tide[1][idx:idx+48]
    tide_time = tide[0][idx:idx+48]
        
    # Get lat,lon of model and create mask for domain (use arbitrary model)
    lut = io.loadmat('{:s}/{:s}_s100_d130_t-10.mat'.format(lut_loc,lut_prefix),squeeze_me=True,variable_names=['Xp','Yp'])    
    swan_lon = lut['Xp']
    swan_lat = lut['Yp']
    swan_latV = swan_lat.ravel()
    swan_lonV = swan_lon.ravel()
    (Nx,Ny) = swan_lon.shape
    
    # Find model points inside domain
    p = path.Path(np.column_stack((lat,lon)))
    mymask = p.contains_points(zip(swan_latV,swan_lonV))
    mymask = mymask.reshape(Nx,Ny)
    lat_bounds = [min(lat), max(lat)]
    lon_bounds = [min(lon), max(lon)]
     
    # Get row and column bounds 
    (row_l,row_u,col_l,col_u) = get_bounds(mymask,lat,lon)
    
    # Initialize
    hs = np.zeros((Nx,Ny,48))
    dp = np.zeros((Nx,Ny,48))
    tm = np.zeros((Nx,Ny,48))
     
    for fh in range(48): # Forecast hour
        
        # Read in LUT output
#        lut_u = np.arange(5,30,5)
#        lut_dir = np.arange(0,350,10)
#        lut_wl = np.arange(-1,5.5,.5)
        
        u_bot = 5*math.floor(hrdps['u'][0][fh]/5)
        u_top = 5*math.ceil(hrdps['u'][0][fh]/5)
        u_dist = hrdps['u'][0][fh]%5/5 # Weight for bot, top weight is 1-weight
        
        dir_bot = 10*math.floor(hrdps['theta'][0][fh]/10)
        dir_top = 10*math.ceil(hrdps['theta'][0][fh]/10)
        dir_dist = hrdps['theta'][0][fh]%10/10 # Weight for bot, top weight is 1-weight
        
        tide_avg = round(tide_forecast[fh])
        
        # Load 4 hsig lut from which to avg
        lut = load_jdf_lut(u_bot,dir_bot,tide_avg,Nx,Ny,lut_loc,lut_prefix)
        hsA = lut['Hsig']
        dpA = lut['Dir']
        tmA = lut['Dir']
        
        lut = load_jdf_lut(u_bot,dir_top,tide_avg,Nx,Ny,lut_loc,lut_prefix)
        hsB = lut['Hsig']
        dpB = lut['Dir']
        tmB = lut['Dir']        
        
        lut = load_jdf_lut(u_top,dir_bot,tide_avg,Nx,Ny,lut_loc,lut_prefix)
        hsC = lut['Hsig']
        dpC = lut['Dir']
        tmC = lut['Dir']
        
        lut = load_jdf_lut(u_top,dir_top,tide_avg,Nx,Ny,lut_loc,lut_prefix)
        hsD = lut['Hsig']
        dpD = lut['Dir']
        tmD = lut['Dir']
        
        # Distances from actual value
        A = np.sqrt(u_dist**2+dir_dist**2)
        B = np.sqrt(u_dist**2+(1.-dir_dist)**2)
        C = np.sqrt((1-u_dist)**2+dir_dist**2)
        D = np.sqrt((1-u_dist)**2+(1-dir_dist)**2)
           
        hs_mean = (B*C*D*hsA+A*C*D*hsB+A*B*D*hsC+A*B*C*hsD)/(B*C*D+A*C*D+A*B*D+A*B*C)
        dp_mean = (B*C*D*dpA+A*C*D*dpB+A*B*D*dpC+A*B*C*dpD)/(B*C*D+A*C*D+A*B*D+A*B*C)
        tm_mean = (B*C*D*tmA+A*C*D*tmB+A*B*D*tmC+A*B*C*tmD)/(B*C*D+A*C*D+A*B*D+A*B*C)
                
        # Set all other locations to NaN
        hs_mean[~mymask] = float('NaN')
        dp_mean[~mymask] = float('NaN')
        tm_mean[~mymask] = float('NaN')
        
        hs[:,:,fh] = hs_mean
        dp[:,:,fh] = dp_mean
        tm[:,:,fh] = tm_mean
    
    # Employ row,col bounds to keep files smaller
    hs = hs[row_l:row_u,col_l:col_u,:]
    tm = tm[row_l:row_u,col_l:col_u,:]
    dp = dp[row_l:row_u,col_l:col_u,:]
    swan_lat = swan_lat[row_l:row_u,col_l:col_u]
    swan_lon = swan_lon[row_l:row_u,col_l:col_u]
    
    # Grid onto a new grid without missing lat,lon values
#    dx = 0.002
#    dy = 0.002*.7
#    new_lon = np.arange(np.nanmin(swan_lon),np.nanmax(swan_lon),dx)
#    new_lat = np.arange(np.nanmin(swan_lat),np.nanmax(swan_lat),dy)
#    new_Lon, new_Lat = np.meshgrid(new_lon,new_lat)
#    (Nx2,Ny2) = new_Lon.shape
#    new_hs = np.zeros((Nx2,Ny2,48))
#    new_dp = np.zeros((Nx2,Ny2,48))
#    new_tm = np.zeros((Nx2,Ny2,48))
#    for fh in range(48):
#        new_hs[:,:,fh] = regrid(swan_lon.ravel(),swan_lat.ravel(),hs[:,:,fh].ravel(),new_Lon,new_Lat)
#        new_dp[:,:,fh] = regrid(swan_lon.ravel(),swan_lat.ravel(),dp[:,:,fh].ravel(),new_Lon,new_Lat)
#        new_tm[:,:,fh] = regrid(swan_lon.ravel(),swan_lat.ravel(),dp[:,:,fh].ravel(),new_Lon,new_Lat)
    
    
#    import matplotlib.pyplot as plt
#    plt.subplot(211)
#    plt.pcolor(swan_lon,swan_lat,hs[:,:,0])
#    plt.subplot(212)
#    plt.pcolor(new_Lon,new_Lat,new_hs[:,:,0])
        
    # Save re-gridded data
#    swan_lat = new_Lat
#    swan_lon = new_Lon
#    hs = new_hs
#    dp = new_dp
#    tm = new_tm    
    
    io.savemat('{:s}/{:s}Wave.mat'.format(save_loc,model_name),{'hs':hs,'dp':dp,'tm':tm,
        'lat':swan_lat,'lon':swan_lon,'lat_limits':lat_bounds,'lon_limits':lon_bounds,
        'lat_boundary':lat,'lon_boundary':lon})    

    # Also save bounds for manifest file
    #with open('{:s}/{:s}_bounds.txt'.format(save_loc,model_name),'w') as file:
    #    file.write('{:10.6f},{:10.6f}\n'.format(lat_bounds[0],lon_bounds[0]))
    #    file.write('{:10.6f},{:10.6f}\n'.format(lat_bounds[1],lon_bounds[1]))

def main():    
    startTime = time.time()
    
    # Get current forecast
    temp = pickle.load(open('current_forecast.pkl','rb'))   
    date_string = temp[0]
    zulu_hour = temp[1]
    
    # Loop over LUT domains
    N = getwaveLUTmeta.getN()
    for nn in range(N):
        (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon) = getwaveLUTmeta.get_lut_meta(nn)        
        print 'Starting {:s} LUT forecast'.format(model_name)
        save_lut_forecast(model_name,hrdps_loc,tide_loc,shared_loc,lut_loc,mask_loc,lut_prefix,date_string,zulu_hour)
        
    
#    #-------------------- Bellingham Bay ----------------------------
#    model_name = 'bellingham'
#    
#    # Inputs+
#    hrdps_loc = '../LUTinputs/BellinghamBay_wind.mat'
#    tide_loc = '../TidePredObs/9449211_pred_navd88.pkl'
#    
#    # Shared Inputs
#    shared_loc = '/media/sf_VMShare'
#    lut_loc = shared_loc + '/SalishSeaLUT/RES1'
#    lut_prefix = 'SpatialJDF'
#    mask_loc = shared_loc + '/OperationalMasks/BellinghamBay.kml'
#
#    # Create and save the spatial wave forecast
#    save_lut_forecast(model_name,hrdps_loc,tide_loc,shared_loc,lut_loc,mask_loc,lut_prefix,date_string,zulu_hour)
#    #----------------------------------------------------------------
#
#    #-------------------- Skagit ----------------------------
#    model_name = 'skagit'
#    
#    # Inputs
#    hrdps_loc = '../LUTinputs/SkagitDelta_wind.mat'
#    tide_loc = '../TidePredObs/9448576_pred_navd88.pkl' #Sneeoosh
#    
#    # Shared Inputs
#    shared_loc = '/media/sf_VMShare'
#    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
#    lut_prefix = 'SpatialPS'
#    mask_loc = shared_loc + '/OperationalMasks/Skagit.kml'
#
#    # Create and save the spatial wave forecast
#    save_lut_forecast(model_name,hrdps_loc,tide_loc,shared_loc,lut_loc,mask_loc,lut_prefix,date_string,zulu_hour)
#    #----------------------------------------------------------------
#
#    #-------------------- Port Susan Bay ----------------------------
#    model_name = 'portsusan'
#    
#    # Inputs
#    hrdps_loc = '../LUTinputs/PortSusan_wind.mat'
#    tide_loc = '../TidePredObs/9448043_pred_navd88.pkl' #Kayak Pt
#    
#    # Shared Inputs
#    shared_loc = '/media/sf_VMShare'
#    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
#    lut_prefix = 'SpatialPS'
#    mask_loc = shared_loc + '/OperationalMasks/PortSusan.kml'
#
#    # Create and save the spatial wave forecast
#    save_lut_forecast(model_name,hrdps_loc,tide_loc,shared_loc,lut_loc,mask_loc,lut_prefix,date_string,zulu_hour)
#    #----------------------------------------------------------------

    print 'Total time elapsed: {0:.2f} minutes'.format(((time.time() - startTime)/60.))
    

if __name__ == "__main__":
    main()    

#plt.plot(swan_lonV,swan_latV,'.')
#plt.plot(lon,lat)
#hs[~mymask] = float('NaN')
#plt.pcolor(swan_lon,swan_lat,hs)






























