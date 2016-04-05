from __future__ import division
import numpy as N
from geotherm.units import u
from heatflow.config import (
    continental_crust,
    oceanic_mantle, interface_depth)

def geobaric_gradient(pressure):
    return pressure/.03 # km

def geobaric_gradient(pressure):
    rho0 = continental_crust.density
    g = u(9.8,'m/s^2')
    P = u(pressure,'GPa')

    rho1 = oceanic_mantle.density
    d0 = u(30,'km')

    a0 = P/g/rho0
    if a0 < d0:
        return a0.to('km')

    a = P/g - rho0*d0 + rho1*d0
    a/=rho1
    return a.to('km')

