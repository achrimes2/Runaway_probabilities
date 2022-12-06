"""
@author: Ashley Chrimes
"""

# Example usage for runaway_calc.
# The extinction module (https://extinction.readthedocs.io/en/latest/) is a pre-requisite.

from runaway_calc import calculate_probability
import numpy as np

#Observatory of choice
choice = input("Enter one of 'Gaia', 'HST', 'JWST' or 'NGRST': ")

#Distance in kpc
distance = np.float(input("Enter a distance in kpc: "))*1000

#Extinction in Av 
Av = np.float(input(r"Enter a visual extinction Av: "))

# Choose your filter. Options available are,
# 'g','r','i','J','H','K' for standard filters in AB mags. 
# Can also choose 'F277W' or 'F444W' for JWST/NIRcam (AB), or...
# Gaia filters; 'G', 'GBP', 'GRP' - these are in Vega mags.
print("Choose a filter. Options are 'g', 'r', 'i', 'J', 'H', 'K' (all AB mags), 'F277W', 'F444W' for JWST (also AB) and for 'G' for Gaia (Vega mags).")
band = input("Enter filter choice: ")

# Enter the limiting magnitude above which detections can be confidently made,
maglim = np.float(input(r"Enter a (3 sigma) limiting magnitude: "))

# Enter the minimum measurable proper motion. This will be overridden for Gaia DR3, HST and JWST in favour of a
# magnitude-dependent model, so you can enter anything.
# For NGRST, whatever you enter here will be used. Nominally 0.01mas/yr is achievable for NGRST.
mu_min = 0.01 #Default value for NGRST, this will be overriden if Gaia, HST or JWST are chosen, and replaced with a mag-dependent model.

#This is the temporal baseline between two images.
#For Gaia and NGRST, this parameter won't be used. For HST, JWST and NGRST, it will.
if choice == 'Gaia' or choice =='NGRST':
    years = -999 #not used
elif choice == 'HST' or choice == 'JWST':
    years = np.float(input("Enter the number of years between images: "))
    


prob = calculate_probability(choice,distance,Av,band,maglim,mu_min,years)

print('Probability of detecting and measuring the motion of an ejected companion associated with this remnant is ',prob)