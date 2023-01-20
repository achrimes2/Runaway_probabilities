Code to calculate the probability of detecting a runaway, as described in Chrimes et al. 2023.

An example script is provided in example_calc.py, which uses the function 'calculate_probability' in runaway_calc.py.

Inputs:
 - Choice (enter either 'Gaia DR3', 'HST', 'JWST', 'Euclid', 'NGRST' or 'custom')
 - Distance [kpc]
 - Av
 - Filter: g,r,i,J,H,K,G, F277W, F444W or (Gaia) G
 - maglim (enter in AB unless Gaia G was chosen for the filter, then use Vega mags)
 - mu_min [mas/yr]
 - Baseline [years]
 - Number of exposures Nexp

Where 'maglim' is the limiting magnitude and 'mu_min' is the minimum measurable proper motion. For all except 'custom' mu_min will be overriden by a magnitide dependent model. The 'years' parameter, the gap between observations, is included in the model is anything other than Gaia. "Nexp" can be specified, more exposures improve reduce positional uncertainties (parameter is not used for Gaia).


For sub-divisions by SN type, or other filters, kick distributions or metallicities (here we assume Z=0.020), feel free to get in touch - a.chrimes@astro.ru.nl.


