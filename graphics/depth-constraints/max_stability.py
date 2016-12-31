# -*- coding: utf-8 -*-
"""
Here we use the experimental results of O'Neill (1981)
to constrain the maximum stable depths for spinel peridotites
with a given equilibrium temperature and spinel chromium content.

This problem is delved into in more detail by Klemme (2004) but
those results are more focused on high pressures and are not used
here. His compilation of thermodynamic constants is used to estimate
the free energy of garnet to compute reaction slopes.
Klemme, 2000 shows that previous results by O'Neill (1981) are sufficiently
accurate for < 1200ºC

Other thermodynamic constants are from Anderson, Thermodynamics of
Natural Systems, Volume 2.
"""
from __future__ import division
import numpy as N

deltaV = 0.7820 # J/bar

temperature = [900,1000,1100] #ºC
equilibrium_pressure_ = [16.7,17.3,18.7] # kbar
coeffs = N.polyfit(temperature,equilibrium_pressure_,2)

def equilibrium_pressure(T):
    """
    Pressure in kbar for a given temperature,
    calibrated between 900 and 1100ºC. Could
    use Klemme 2000 correction, but this is more complex.
    """
    return coeffs[0]*(T**2)+coeffs[1]*T+coeffs[2]

def pressure(T,XCr_sp=0):
    a = 27.9 # kbar
    P0 = equilibrium_pressure(T)
    return (P0+a*XCr_sp)/10 # result to GPa

def max_depth(*args):
    return pressure(*args)/.03

