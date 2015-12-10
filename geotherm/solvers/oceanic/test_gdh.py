# -*- coding: utf-8 -*-
"""
This module contains a naive implementation of GDH
for testing purposes.

GDH variables:
L   95        ºC    Plate thickness
Ta  1450      ºC    Asthenospheric temperature
a   3.1e-5    1/ºC  Coefficient of thermal expansion
km  3.138     W/m   Thermal conductivity
cp  1.171     kJ/kg Specific heat
K   0.804e-6  m^2/s Thermal diffusivity
pm  3330      kg/m3 Mantle density
pw  1000      kg/m3 Water density
dr  2.6       km    Ridge depth
"""

from __future__ import division
import numpy as N

from ...models import Material


def gdh_temperature(depth, time, order=50, **kwargs):
    """This equation is simplified to ignore horizontal heat conduction"""

    Ta = 1450
    L = 95
    K = 0.804e-6

    time *= 3.15569e7
    def summation_term(n):
        ex = (n*N.pi/L)**2
        return 2 / (n*N.pi) * N.sin(n*N.pi*depth/L) * N.exp(-ex*K*time)

    taylor_expansion = N.array([summation_term(i+1) for i in range(order)])

    sol = Ta * (depth/L + N.sum(taylor_expansion, axis=0))
    return sol

gdh_mantle = Material

def test_gdh_temperature():
    assert gdh_temperature(0,0) == 0
    assert False
