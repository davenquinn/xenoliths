#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sys import argv

a  = float(argv[1])

from IPython import embed
import numpy as N
from geotherm.units import u

def geobaric_gradient(pressure):
    return pressure/.03 # km

def geobaric_gradient2(pressure):
    rho0 = u(2.8,'g/cm^3')
    g = u(9.8,'m/s^2')
    P = u(pressure,'GPa')

    rho1 = u(3.3,'g/cm^3')
    d0 = u(30,'km')

    a0 = P/g/rho0
    if a0 < d0:
        return a0.to('km')

    a = P/g - rho0*d0 + rho1*d0
    a/=rho1
    return a.to('km')

print geobaric_gradient(a)
print geobaric_gradient2(a)
