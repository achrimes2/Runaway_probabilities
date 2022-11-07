#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ashley Chrimes
"""

# Usage example for eunaway_calc.

from runaway_calc import calculate_probability

#Distance in pc
distance = 8500

#Extinction in Av 
Av = 5.4

# The filter in question.
# Enter 'g','r','i','J','H','K' for standard filters in AB mags. 
# Can also use Gaia filters; 'G', 'GBP', 'GRP' - these are in Vega mags.
band = 'F277W'  

# Enter the limiting magnitude above which detections can be confidently made,
maglim = 26

# Enter the minimum measurable proper motion,
pmlim = 1

prob = calculate_probability(distance,Av,band,maglim,pmlim)

print('Probability of detecting and measuring the motion of an ejected companion associated with this remnant is ',prob)