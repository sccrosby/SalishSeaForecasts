#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 10:44:28 2018
Reads in HRDPS and extracts desired winds/pressure
@author: s. c. crosby
"""
import pygrib
import numpy as np
import time
import pickle
from scipy import io
from pyproj import Proj

# Location to save output
fol_output = '../LUTinputs'

# Location of HRDPS
fol_hrdps = '../hrdps'

# Static HRDPS information
hrdps_PrefixP           = 'CMC_hrdps_west_PRMSL_MSL_0_ps2.5km_' 
hrdps_PrefixU           = 'CMC_hrdps_west_UGRD_TGL_10_ps2.5km_'
hrdps_PrefixV           = 'CMC_hrdps_west_VGRD_TGL_10_ps2.5km_'
hrdps_PrefixLAND        = 'CMC_hrdps_west_LAND_SFC_0_ps2.5km_'
hrdps_lamwest_file      = '../hrdps/lamwestpoints.dat'
hrdps_rotation_file     = '../hrdps/rotations.dat'
num_forecast_hours      = 48


def read_hrdps_grib(date_string, zulu_hour):
    
    # Initialize        
    grib_input_loc = '{0:s}/{1:s}/'.format(fol_hrdps,date_string)
    #bounds = param['crop_bounds']
    
    #----------------------- Load up HRDP Land Mask----------------------------------------
    maskFileName = '{0:s}/{1:s}{2:s}{3:02d}_P000-00.grib2'.format(grib_input_loc, hrdps_PrefixLAND, date_string, zulu_hour)
    grbl = pygrib.open(maskFileName)
    grblL = grbl.select(name='Land-sea mask')[0]
    Land = grblL.values
    Land = np.asarray(Land)
    Ny = np.shape(Land)[0]
    Nx = np.shape(Land)[1]
    #Land = Land[bounds[0,1]:bounds[1,1], bounds[0,0]:bounds[1,0]]    # reduce to Salish Sea region
    
    #------------------------------- Load lat/lon positions of hrps ---------------------------------
    degreesLat = np.zeros((Ny,Nx), dtype='d')
    degreesLon = np.zeros((Ny,Nx), dtype='d')
    indexFile = open(hrdps_lamwest_file,'r')
    for line in indexFile:
        split = line.split()
        i = int(split[0])-1
        j = int(split[1])-1
        degreesLat[j,i] = float(split[2])
        degreesLon[j,i] = float(split[3])
    indexFile.close()
    #degreesLat = degreesLat[bounds[0,1]:bounds[1,1], bounds[0,0]:bounds[1,0]]
    #degreesLon = degreesLon[bounds[0,1]:bounds[1,1], bounds[0,0]:bounds[1,0]]
    
    #---------------------------- Load rotations---------------------
    Theta = load_rotations(hrdps_rotation_file,Ny,Nx)
    #Theta = Theta[bounds[0,1]:bounds[1,1], bounds[0,0]:bounds[1,0]]
    Nyr = np.shape(Theta)[0]
    Nxr = np.shape(Theta)[1]
    
    
    #--------------------------------------------- UTM ----------------------------------------------
    # p = Proj(proj='utm', zone=10, ellps='WGS84')
    # X, Y = p(degreesLon, degreesLat)  # note the capital L
    
    
    # ------------ Load in All Forecast Data --------------------------------
    U10 = np.zeros([485,685,48])
    V10 = np.zeros([485,685,48])
    SLP = np.zeros([485,685,48])
    for hour in range(num_forecast_hours):
        #Input grib file names            
        UwindFileName = '{0:s}{1:s}{2:s}{3:02d}_P{4:03d}-00.grib2'.format(grib_input_loc, hrdps_PrefixU, date_string, zulu_hour, hour)
        VwindFileName = '{0:s}{1:s}{2:s}{3:02d}_P{4:03d}-00.grib2'.format(grib_input_loc, hrdps_PrefixV, date_string, zulu_hour, hour)
        PresFileName = '{0:s}{1:s}{2:s}{3:02d}_P{4:03d}-00.grib2'.format(grib_input_loc, hrdps_PrefixP, date_string, zulu_hour, hour)
        
        # Open grib
        grbsu = pygrib.open(UwindFileName)
        grbu  = grbsu.select(name='10 metre U wind component')[0]
        grbsv = pygrib.open(VwindFileName)
        grbv  = grbsv.select(name='10 metre V wind component')[0]
        grbsv = pygrib.open(PresFileName)
        grbp  = grbsv.select(name='Pressure reduced to MSL')[0]
        
        u10 = grbu.values # same as grb['values']
        v10 = grbv.values
        slp = grbp.values
        u10 = np.asarray(u10)
        v10 = np.asarray(v10)
        slp = np.asarray(slp)
        
        # Crop
        #u10 = u10[bounds[0,1]:bounds[1,1], bounds[0,0]:bounds[1,0]]
        #v10 = v10[bounds[0,1]:bounds[1,1], bounds[0,0]:bounds[1,0]]
        
        
        # Rotate to earth relative with Bert-Derived rotations based on grid poitns (increased accuracy was derived for grid locations)
#        for j in range(Nyr):
#            for i in range(Nxr):
#                R = np.matrix([ [np.cos(Theta[j,i]), -np.sin(Theta[j,i])], [np.sin(Theta[j,i]), np.cos(Theta[j,i])] ])
#                rot = R.dot([u10[j,i],v10[j,i]])
#                u10[j,i] = rot[0,0]
#                v10[j,i] = rot[0,1]

        u10 = np.multiply(np.cos(Theta),u10) + np.multiply(-np.sin(Theta),v10)
        v10 = np.multiply(np.sin(Theta),u10) + np.multiply(np.cos(Theta),v10)
                  
        
        # Save all varaibles into list of arrays        
        U10[:,:,hour] = u10
        V10[:,:,hour] = v10
        SLP[:,:,hour] = slp
    
    
    return (degreesLon, degreesLat, U10, V10, SLP)


# Small function to load rotations needed for HRDPS
def load_rotations(hrdps_rotation_file,Ny,Nx):
    Theta = np.zeros((Ny,Nx), dtype='d')
    RotationFile = open(hrdps_rotation_file,'r')
    Lines = RotationFile.readlines()
    RotationFile.close()
    for Line in Lines:
        LineSplit = Line.split()
        i = int(LineSplit[0])
        j = int(LineSplit[1])
        Theta[j,i] = -float(LineSplit[2])
    return Theta


def main():
    # Start timer
    start_time = time.time()
    
    # Get current forecast
    temp = pickle.load(open('current_forecast.pkl','rb'))   
    date_string = temp[0]
    zulu_hour = temp[1]
    
    pt_name = ['BellinghamBay','SkagitDelta','PortSusan']
    pt_lon = [-122.565234, -122.512193, -122.413508]
    pt_lat = [48.715758, 48.338880, 48.172197]
        
    (Lon, Lat, U10, V10, SLP) = read_hrdps_grib(date_string, zulu_hour)
    
    io.savemat('LUToutputs/hrdps_complete_wind_pressure',{'u':U10,'v':V10,'slp':SLP,'lon':Lon,'lat':Lat,'forecast_date':date_string,'forecast_hour':zulu_hour})
    
    # Find closest model grid cell to ndbc
    for nn in range(len(pt_lon)):     
        dist = np.add(np.square(np.array(Lon)-pt_lon[nn]),np.square(np.array(Lat)-pt_lat[nn]))
        (I_lon, I_lat) = np.where(dist == np.min(dist))   
        
        # Extract point velocities
        ui = U10[I_lon,I_lat][0]
        vi = V10[I_lon,I_lat][0]
        slp = SLP[I_lon,I_lat][0]
        
        # Est magnitude and direction
        u = np.sqrt(ui**2 + vi**2)
        theta = 90 - 180/np.pi*np.arctan2(vi,ui) + 180
        theta[theta>360] = theta[theta>360]-360
        theta[theta<0] = theta[theta<0]+360 
        
        # Save
        outfile = '{0:s}/{1:s}_wind'.format(fol_output,pt_name[nn])
        io.savemat(outfile,{'u':u,'theta':theta,'slp':slp,'date_string':date_string,'zulu_hour':zulu_hour})
    
    print 'Total time elapsed: {0:.2f} minutes'.format(((time.time() - start_time)/60.))
    

if __name__ == "__main__":
    main()
   
    


    

    
    
    
    
