"""
@author: Ashley Chrimes
"""

# Code for calculating the probability that a runaway/walkaway can be detected for a given survey/dataset. 

# Prerequisites: the extinction module (https://extinction.readthedocs.io/en/latest/).

# Uses prepared outputs from BPASS, and binary SNe kick calculations, as described in Chrimes et al. 2023.

# Results only provided for all SNe and at Solar metallicity, SN subtypes and other metallicities can be provided upon request.

import numpy as np
import extinction

def calculate_probability(choice,distance,Av,band,maglim,mu_min,years):

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
    can_see = mags[cond2]
    
    if choice == 'Gaia': #implementing mag-dependent mu_min for Gaia
        Tfactor = 1 
        z = np.max([10**(0.4*(13-15)), 10**(0.4*(np.median(can_see)-15))]) 
        sig_omega_bar = Tfactor * np.sqrt(40 + 800*z + 30*(z**2))
        #For Gaia ER3 we have
        mu_min = 0.96*sig_omega_bar/1000 #divided by 1000 to get mas/yr

        
    elif choice == 'HST':
        FWHM = 0.14 #asec
        sigma = (1/3)*10**(-(maglim)/2.5) #assuming 3 sigma limiting mag
        SNR = (1/sigma) * 10**(-(np.median(can_see))/2.5)
        sig_pos = FWHM/(2.35*SNR)
        pixel = 0.065 #typical for a 3-dither drizzled WFC3/IR image, asec/pixel
        if sig_pos < 0.03*pixel: #limited by fact image is pixelated
            sig_pos = 0.03*pixel
        sig_abs = 0.05/1000 #asec, e.g. typical rms for tie to Gaia for absolute astrometry
        sig_tot = np.sqrt(sig_pos**2 + sig_abs**2)
        theta_min = np.sqrt( 2*(sig_tot)**2 )/years
        mu_min = theta_min*1000/years  #into mas/yr for 1 sigma uncertainty on mu
    
    elif choice == 'JWST':
        FWHM = 0.09 #asec
        sigma = (1/3)*10**(-(maglim)/2.5) #assuming 3 sigma limiting mag
        SNR = (1/sigma) * 10**(-(np.median(can_see))/2.5)
        sig_pos = FWHM/(2.35*SNR)
        pixel = 0.063 #native NIRcam pixel scale in 2.4mu-5.0mu range, asec/pixel
        if sig_pos < 0.03*pixel: #limited by fact image is pixelated
            sig_pos = 0.03*pixel
        sig_abs = 0.05/1000 #asec, e.g. typical rms for tie to Gaia for absolute astrometry
        sig_tot = np.sqrt(sig_pos**2 + sig_abs**2)
        theta_min = np.sqrt( 2*(sig_tot)**2 )/years
        mu_min = theta_min*1000/years  #into mas/yr for 1 sigma uncertainty on mu
    
    elif choice == 'NGRST':
        mu_min = 0.01 #mas/yr
        
    dpc = distance*(3.0857*10**16)                          #distance pc -> m
    radians_per_year = 2*np.pi*(((mu_min/1000)/3600)/360)      #min PM from mas -> rad/yr
    vel_m_per_year = radians_per_year * dpc   #rad/yr -> metres per year
    kms = (vel_m_per_year/1000)/(365*24*3600)       #m/yr -> km/s

    condfrac = (TOT2D[cond1] > kms) & cond2       #PM & mag limits applied: fast enough & bright enough to see & detect motion
    probability = 0.45*np.sum(weights[cond1][condfrac])/np.sum(weights[cond1])  #Probability of detection and motion measurement
    #A factor of 0.45 is include because only 45% of all CCSNe predicted to arise from primaries.
    #The rest are from single stars, merged binaries, ejected secondaries or secondaries with a compact remnant, no ejected companion.

    return np.round(probability,3)
