#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 15:15:31 2018

@author: crosby
"""

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


# Location to save output
fol_output = '../gdps/PostProcessed'

# Location of HRDPS
fol_gdps = '../gdps'

# Static HRDPS information
gdps_PrefixP           = 'CMC_glb_PRMSL_MSL_0_latlon.24x.24_' 
gdps_PrefixU           = 'CMC_glb_UGRD_TGL_10_latlon.24x.24_'
gdps_PrefixV           = 'CMC_glb_VGRD_TGL_10_latlon.24x.24_'
gdps_PrefixLAND        = 'CMC_glb_LAND_SFC_0_latlon.24x.24_'
gdps_url               = 'http://dd.weather.gc.ca/model_gem_global/25km/grib2/lat_lon/'

# Set forecast hours
forecast_hours =  range(0,243,3)
num_forecast_hours = len(forecast_hours)

# Set grid (from web description) (lat,lon format)
lat = np.arange(-90.,90.24,0.24)
lat = lat[0:-1]
lon = np.arange(-180,180,.24)

# Set crop
ind_lat = np.logical_and(lat>45,lat<52)
ind_lon = np.logical_and(lon>-130,lon<-120)

lon = lon[ind_lon]
lat = lat[ind_lat]
Ny = len(lat)
Nx = len(lon)

def sub2ind(array_shape, rows, cols):
    ind = rows*array_shape[1] + cols
    ind[ind < 0] = -1
    ind[ind >= array_shape[0]*array_shape[1]] = -1
    return ind

def read_gdps_grib(date_string, zulu_hour):
    
    # Initialize        
    grib_input_loc = '{0:s}/{1:s}/'.format(fol_gdps,date_string)   
              
    # ------------ Load in All Forecast Data --------------------------------
    #U10 = np.zeros([Ny,Nx,num_forecast_hours])
    #V10 = np.zeros([Ny,Nx,num_forecast_hours])
    SLP = np.zeros([Ny,Nx,num_forecast_hours])
    for hh in range(num_forecast_hours):
        #Input grib file names            
        #UwindFileName = '{0:s}{1:s}{2:s}{3:02d}_P{4:03d}.grib2'.format(grib_input_loc, hrdps_PrefixU, date_string, zulu_hour, hour)
        #VwindFileName = '{0:s}{1:s}{2:s}{3:02d}_P{4:03d}.grib2'.format(grib_input_loc, hrdps_PrefixV, date_string, zulu_hour, hour)
        PresFileName = '{0:s}{1:s}{2:s}{3:02d}_P{4:03d}.grib2'.format(grib_input_loc, gdps_PrefixP, date_string, zulu_hour, forecast_hours[hh])
        
        # Open grib
#        grbsu = pygrib.open(UwindFileName)
#        grbu  = grbsu.select(name='10 metre U wind component')[0]
#        grbsv = pygrib.open(VwindFileName)
#        grbv  = grbsv.select(name='10 metre V wind component')[0]
        grbsv = pygrib.open(PresFileName)
        grbp  = grbsv.select(name='Pressure reduced to MSL')[0]
        
#        u10 = grbu.values # same as grb['values']
#        v10 = grbv.values
        slp = grbp.values
#        u10 = np.asarray(u10)
#        v10 = np.asarray(v10)
        slp = np.asarray(slp)
        slp = slp[ind_lat,:]
        slp = slp[:,ind_lon]
        
        
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

        #u10 = np.multiply(np.cos(Theta),u10) + np.multiply(-np.sin(Theta),v10)
        #v10 = np.multiply(np.sin(Theta),u10) + np.multiply(np.cos(Theta),v10)
                  
        
        # Save all varaibles into list of arrays        
        #U10[:,:,hour] = u10
        #V10[:,:,hour] = v10
        SLP[:,:,hh] = slp
    
    
    return SLP



def main():
    # Start timer
    start_time = time.time()
    
    # Get current forecast
    temp = pickle.load(open('current_forecast_gdps.pkl','rb'))   
    date_string = temp[0]
    zulu_hour = temp[1]
    
    pt_name = ['BellinghamBay','SkagitDelta','PortSusan']
    pt_lon = [-122.565234, -122.512193, -122.413508]
    pt_lat = [48.715758, 48.338880, 48.172197]
        
    SLP = read_gdps_grib(date_string, zulu_hour)
    
    io.savemat('{:s}/gdps_pressure_spatial'.format(fol_output),
               {'slp':SLP,'lon':lon,'lat':lat,'forecast_date':date_string,'forecast_hour':zulu_hour})
    
    # Find closest model grid cell to ndbc
    [Lon,Lat] = np.meshgrid(lon,lat)
    for nn in range(len(pt_lon)):     
        dist = np.add(np.square(np.array(Lon)-pt_lon[nn]),np.square(np.array(Lat)-pt_lat[nn]))
        (I_lon, I_lat) = np.where(dist == np.min(dist))   
        
        # Extract point velocities
        #ui = U10[I_lon,I_lat][0]
        #vi = V10[I_lon,I_lat][0]
        slp = SLP[I_lon,I_lat,:]
        
        # Est magnitude and direction
#        u = np.sqrt(ui**2 + vi**2)
#        theta = 90 - 180/np.pi*np.arctan2(vi,ui) + 180
#        theta[theta>360] = theta[theta>360]-360
#        theta[theta<0] = theta[theta<0]+360 
        
        # Save
        outfile = '{0:s}/{1:s}_gdps_slp'.format(fol_output,pt_name[nn])
        io.savemat(outfile,{'slp':slp,'date_string':date_string,'zulu_hour':zulu_hour})
    
    print 'Total time elapsed: {0:.2f} minutes'.format(((time.time() - start_time)/60.))
    

if __name__ == "__main__":
    main()
   
    


    

    
    
    
    
