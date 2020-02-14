#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:32:49 2019

@author: crosby
"""

# Number of LUT predictions
def getN():
    return 8

def bellingham():
    # Bellingham
    model_name = 'bellingham'    
    # Inputs
    hrdps_loc = '../LUTinputs/bellingham_wind.mat'
    tide_loc = '../TidePredObs/9449211_pred_navd88.pkl'    
    # External Inputs (LUT + masks)
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES1'
    lut_prefix = 'SpatialJDF'
    mask_loc = shared_loc + '/OperationalMasks/BellinghamBay.kml'
    lat = 48.715758
    lon = -122.565234
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def skagit():
    model_name = 'skagit'    
    # Inputs
    hrdps_loc = '../LUTinputs/skagit_wind.mat'
    tide_loc = '../TidePredObs/9448576_pred_navd88.pkl' #Sneeoosh    
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/Skagit.kml'
    lat = 48.338880
    lon = -122.512193
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)    
    
def portsusan():
    model_name = 'portsusan'    
    # Inputs
    hrdps_loc = '../LUTinputs/portsusan_wind.mat'
    tide_loc = '../TidePredObs/9448043_pred_navd88.pkl' #Kayak Pt    
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/PortSusan.kml'
    lat = 48.172197
    lon = -122.413508
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def admiralty():
    model_name = 'admiralty'    
    # Inputs
    hrdps_loc = '../LUTinputs/admiralty_wind.mat'
    tide_loc = '../TidePredObs/9444900_pred_navd88.pkl' #Porttownsend    
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/admiralty.kml'
    lat = 47.989021
    lon = -122.622876
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def nisqually():
    model_name = 'nisqually'    
    # Inputs
    hrdps_loc = '../LUTinputs/nisqually_wind.mat'
    tide_loc = '../TidePredObs/9446828_pred_navd88.pkl' #Nisqually
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/nisqually.kml'
    lat = 47.115375
    lon = -122.708310
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def seattle():
    model_name = 'seattle'    
    # Inputs
    hrdps_loc = '../LUTinputs/seattle_wind.mat'
    tide_loc = '../TidePredObs/9447130_pred_navd88.pkl' #Seattle
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/seattle.kml'
    lat = 47.624916
    lon = -122.451151
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def tacoma():
    model_name = 'tacoma'    
    # Inputs
    hrdps_loc = '../LUTinputs/tacoma_wind.mat'
    tide_loc = '../TidePredObs/9446484_pred_navd88.pkl' #Tacoma
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/tacoma.kml'
    lat = 47.318624
    lon = -122.464596
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def westcamano():
    model_name = 'westcamano'    
    # Inputs
    hrdps_loc = '../LUTinputs/westcamano_wind.mat'
    tide_loc = '../TidePredObs/9447929_pred_navd88.pkl' #PennCove
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/westcamano.kml'
    lat = 48.227197
    lon = -122.579435
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def caseinlet():
    model_name = 'westcamano'    
    # Inputs
    hrdps_loc = '../LUTinputs/caseinlet_wind.mat'
    tide_loc = '../TidePredObs/9446484_pred_navd88.pkl' #Tacoma
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/LUT_domains/westcamano.kml'
    lat = 47.283341
    lon = -122.838442
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def southhood():
    model_name = 'southhood'    
    # Inputs
    hrdps_loc = '../LUTinputs/southhood_wind.mat'
    tide_loc = '../TidePredObs/9444900_pred_navd88.pkl' #Porttownsend  
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/LUT_domains/southhood.kml'
    lat = 47.436116
    lon = -123.104426
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def northhood():
    model_name = 'northhood'    
    # Inputs
    hrdps_loc = '../LUTinputs/northhood_wind.mat'
    tide_loc = '../TidePredObs/9444900_pred_navd88.pkl' #Porttownsend  
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/LUT_domains/northhood.kml'
    lat = 47.690429
    lon = -122.862342
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def carrinlet():
    model_name = 'carrinlet'    
    # Inputs
    hrdps_loc = '../LUTinputs/carrinlet_wind.mat'
    tide_loc = '../TidePredObs/9446828_pred_navd88.pkl' #Nisqually
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/LUT_domains/carrinlet.kml'
    lat = 47.265720
    lon = -122.704912
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def eastvashon():
    model_name = 'eastvashon'    
    # Inputs
    hrdps_loc = '../LUTinputs/eastvashon_wind.mat'
    tide_loc = '../TidePredObs/9446828_pred_navd88.pkl' #Nisqually
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/LUT_domains/eastvashon.kml'
    lat = 47.400971
    lon = -122.538643
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

def sog():
    model_name = 'sog'    
    # Inputs
    hrdps_loc = '../LUTinputs/sog_wind.mat'
    tide_loc = '../TidePredObs/9449211_pred_navd88.pkl'    #Bellingham
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/LUT_domains/sog.kml'
    lat = 48.884530
    lon = -123.095271
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)


def padilla():
    model_name = 'padilla'    
    # Inputs
    hrdps_loc = '../LUTinputs/padilla_wind.mat'
    tide_loc = '../TidePredObs/9449211_pred_navd88.pkl'    #Bellingham
    # Shared Inputs
    shared_loc = '/media/sf_VMShare'
    lut_loc = shared_loc + '/SalishSeaLUT/RES2'
    lut_prefix = 'SpatialPS'
    mask_loc = shared_loc + '/OperationalMasks/LUT_domains/padilla.kml'
    lat = 48.543383
    lon = -122.556331
    return (model_name, hrdps_loc, tide_loc, shared_loc, lut_loc, lut_prefix, mask_loc, lat, lon)

    
def get_lut_meta(arg):
    switcher = {
            0: bellingham,
            1: skagit,
            2: portsusan,
            3: admiralty,
            4: nisqually,
            5: seattle,
            6: tacoma,
            7: westcamano,
            8: caseinlet,
            9: southhood,
            10: northhood,
            11: carrinlet,
            12: eastvashon,
            13: sog,
            14: padilla                        
        }
    # Get the function from the switch dic 
    func = switcher.get(arg, lambda: "Invalid Model")
    # Exectue
    return func()

