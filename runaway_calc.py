#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ashley Chrimes
"""

# Code for calculating the probability that a runaway/walkaway can be detected for a given survey/dataset. 

# Prerequisites: the extinction module (https://extinction.readthedocs.io/en/latest/).

# Uses prepared outputs from BPASS, and binary SNe kick calculations, as described in Chrimes et al. 2023 (?)

# Inputs: distance (pc), extinction (Av), 

# Results only provided for all SNe and at Solar metallicity, SN subtypes and other metallicities can be provided upon request.

import numpy as np
import extinction

def calculate_probability(distance,Av,band,maglim,pmlim):

    filterinfo = np.loadtxt('filters.txt',dtype='str')    #Load in filter details.
    
    row = np.where(filterinfo[:,0] == band)[0][0]      #Identify the appropriate row for the chosen filter.
    
    wave = np.array([np.float(filterinfo[row,1])])     #Effective wavelength of filter chosen.
    
    filename = filterinfo[row,2]                     #Filter name (for opening magnitude files) chosen.
    
    metals = 'z020'                                   #Currently only Solar Z provided (Z = 0.020)
    root = 'SN_ALL/'                                  #Currently all SNe provided, not split by SN type
    
    #Selecting the model weightings.
    #Each runaway model has photometry and a weighting, and appears N times, 
    if band != 'F277W' and band != 'F444W':
        weights = np.loadtxt(root+'bin_'+metals+'_weight_frac_unbound.txt')   #each appearance represents a different random NS kick.
        TOT2D = np.loadtxt(root+'total2dvelprojected.txt')     #transverse velocities in km/s
    else:
        weights = np.loadtxt(root+'bin_'+metals+'_Wjwst_unbound.txt')  
        TOT2D = np.loadtxt(root+'bin_z020_Vjwst_unbound.txt')     #transverse velocities in km/s
    
    magnitudes = np.loadtxt(root+'bin_'+metals+'_'+filename+'_unbound.txt') #the absolute magnitudes.
    cond1 = (magnitudes < 30) #removes any spurious entries.
    
    Aband = extinction.fitzpatrick99(wave, Av, 3.1)     #Extinction in the chosen filter, derived from Rv=3.1, Fitzpatrick 99, Av & effective wavelength

    mags = 5*np.log10(distance/10) + magnitudes[cond1] + Aband    #Apparent magnitudes constructed using extinction & distance
    cond2 = (mags < maglim)                               #Limititng magnitude applied. Which mags are detectable?
    
    dpc = distance*(3.0857*10**16)                          #distance pc -> m
    radians_per_year = 2*np.pi*(((pmlim/1000)/3600)/360)      #min PM from mas -> rad/yr
    vel_m_per_year = radians_per_year * dpc   #rad/yr -> metres per year
    kms = (vel_m_per_year/1000)/(365*24*3600)       #m/yr -> km/s

    condfrac = (TOT2D[cond1] > kms) & cond2       #PM & mag limits applied: fast enough & bright enough to see & detect motion
    probability = 0.45*np.sum(weights[cond1][condfrac])/np.sum(weights[cond1])  #Probability of detection and motion measurement
    #A factor 0.45 is include because only 45% of all CCSNe predicted to arise from primaries.
    #The rest are from single stars, merged binaries, ejected secondaries or secondaries with a compact remnant, no ejected companion.

    return probability
