Code to calculate the probability of detecting a runaway, as described in Chrimes et al. 2023.

An example is shown in example_calc.py, which used the function 'calculate_probability' in runaway_calc.py.

Inputs:
Choice (enter either 'Gaia DR3', 'HST', 'JWST' or 'NGRST')
Distance [pc]
Av
Filter (g,r,i,J,H,K,G,GBP, GRP, F277W or F444W)
maglim 
mu_min [mas/yr]

Where 'maglim' is the limiting magnitude and 'mu_min' is the minimum measurable proper motion. mu_min will be overriden by a magnitide dependent model if
anything other than choice='NGRST'. The 'years' parameter is included in the model if choice='HST' or 'JWST'.

N.b. Gaia magnitudes are in the Vega system, others are in AB.

For sub-divisions by SN type, or other filters, kick distributions or metallicities (here we assume Z=0.020), feel free to get in touch - a.chrimes@astro.ru.nl.


