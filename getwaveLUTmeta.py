#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:32:49 2019

@author: crosby
"""

# Number of LUT predictions
def getN():
    return 3

def bellingham():
    # Bellingham
    model_name = 'bellingham'    
    # Inputs
    hrdps_loc = '../LUTinputs/BellinghamBay_wind.mat'
    tide_loc = '../TidePredObs/9449211_pred_navd88.pkl'    
    # External Inputs (LUT + masks)
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES1'
    lut_prefix = 'SpatialJDF'
    mask_loc = shared_loc + '/OperationalMasks/BellinghamBay.kml'
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc)

def skagit():
    model_name = 'skagit'    
    # Inputs
    hrdps_loc = '../LUTinputs/SkagitDelta_wind.mat'
    tide_loc = '../TidePredObs/9448576_pred_navd88.pkl' #Sneeoosh    
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/Skagit.kml'
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc)    
    
def portsusan():
    model_name = 'portsusan'    
    # Inputs
    hrdps_loc = '../LUTinputs/PortSusan_wind.mat'
    tide_loc = '../TidePredObs/9448043_pred_navd88.pkl' #Kayak Pt    
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/PortSusan.kml'
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc)
    
def get_lut_meta(arg):
    switcher = {
            0: bellingham,
            1: skagit,
            2: portsusan,
        }
    # Get the function from the switch dic 
    func = switcher.get(arg, lambda: "Invalid Model")
    # Exectue
    return func()

