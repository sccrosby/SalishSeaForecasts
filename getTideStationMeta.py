#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 15:57:11 2018

Retrieve location list for stations

@author: crosby
"""

# Full location info 
Lsta_id = {
        'bellingham':'9449211',
        'sneeoosh':'9448576',
        'kayakpoint':'9448043',
        'nisqually':'9446828',
        'tacoma':'9446484',
        'seattle':'9447130',
        'porttownsend':'9444900'}

Lxtide_str = {
        'bellingham':'Bellingham, Bellingham Bay, Washington',
        'sneeoosh':'Sneeoosh Point, Washington',
        'kayakpoint':'Kayak Point, Washington',
        'nisqually':'Dupont Wharf, Nisqually Reach, Puget Sound, Washington',
        'tacoma':'Tacoma, Commencement Bay, Sitcum Waterway, Puget Sound, Washington',
        'seattle':'Seattle, Puget Sound, Washington',
        'porttownsend':'Port Townsend (Point Hudson), Admiralty Inlet, Washington'}

Lmllw2navd88 = {
        'bellingham':0.161,
        'sneeoosh':0.582,
        'kayakpoint':0.652,
        'nisqually':1.151,
        'tacoma':0.729,
        'seattle':0.865,
        'porttownsend':0.336}

Llat = {
        'bellingham':48+44.7/60,
        'sneeoosh':48+24/60,
        'kayakpoint':48+8.2/60,
        'nisqually':47.1183,
        'tacoma':47.2667,
        'seattle':47.6206,
        'porttownsend':48.1129}

Llon = {
        'bellingham':-122-29.7/60,
        'sneeoosh':-122-32.9,
        'kayakpoint':-122-22/60,
        'nisqually':-122.6650,
        'tacoma':-122.4133,
        'seattle':-122.3393,
        'porttownsend':-122.7595}


pred_list = ['bellingham','sneeoosh','kayakpoint','nisqually']
obs_list = ['tacoma','seattle','porttownsend']

def get_meta(mylist):
    sta_id = dict((k,Lsta_id[k]) for k in mylist)
    xtide_str = dict((k,Lxtide_str[k]) for k in mylist)
    mllw2navd88 = dict((k,Lmllw2navd88[k]) for k in mylist)
    lat = dict((k,Llat[k]) for k in mylist)
    lon = dict((k,Llon[k]) for k in mylist)
    return (mylist, sta_id, xtide_str,mllw2navd88,lat,lon)

def get_pred():
    return get_meta(pred_list)
    
def get_obs():
    return get_meta(obs_list)

def get_all():
    return get_meta(obs_list+pred_list)







