"""
@author: Ashley Chrimes
"""

# Example usage for runaway_calc.
# The extinction module (https://extinction.readthedocs.io/en/latest/) is a pre-requisite.

from runaway_calc import calculate_probability

#Observatory of choice
choice = 'NGRST'

#Distance in pc
distance = 8500

#Extinction in Av 
Av = 5.4

# Choose your filter. Options available are,
# 'g','r','i','J','H','K' for standard filters in AB mags. 
# Can also choose 'F277W' or 'F444W' for JWST/NIRcam (AB), or...
# Gaia filters; 'G', 'GBP', 'GRP' - these are in Vega mags.
band = 'F277W'  

# Enter the limiting magnitude above which detections can be confidently made,
maglim = 26

# Enter the minimum measurable proper motion. This will be overridden for Gaia DR3, HST and JWST in favour of a
# magnitude-dependent model, so you can enter anything.
# For NGRST, whatever you enter here will be used. Nominally 0.01mas/yr is achievable for NGRST.
mu_min = 0.01

#This is the temporal baseline between two images.
#For Gaia and NGRST, this parameter won't be used. For HST, JWST and NGRST, it will.
years = 5

prob = calculate_probability(choice,distance,Av,band,maglim,mu_min,years)

print('Probability of detecting and measuring the motion of an ejected companion associated with this remnant is ',prob)