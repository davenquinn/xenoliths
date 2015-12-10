# -*- coding: utf-8 -*-
from __future__ import division
import numpy as N

from . import HalfSpaceSolver, GDHSolver
from ...models import Material
from ...units import u

def gdh_temperature(time, depth, order=50, **kwargs):
    """
    Naive implementation of GDH for testing purposes.

    GDH variables:
    L   95        ºC    Plate thickness
    Ta  1450      ºC    Asthenospheric temperature
    a   3.1e-5    1/ºC  Coefficient of thermal expansion
    km  3.138     W/m/K Thermal conductivity
    cp  1.171     kJ/kg Specific heat
    K   0.804e-6  m^2/s Thermal diffusivity
    pm  3330      kg/m3 Mantle density
    pw  1000      kg/m3 Water density
    dr  2.6       km    Ridge depth
    """

    Ta = 1450
    L = 95
    K = 0.804e-6

    time *= 3.15569e7
    def summation_term(n):
        ex = (n*N.pi/L)**2
        return 2 / (n*N.pi) * N.sin(n*N.pi*depth/L) * N.exp(-ex*K*time)

    taylor_expansion = N.array([summation_term(i+1) for i in range(order)])

    return Ta * (depth/L + N.sum(taylor_expansion, axis=0))

gdh_mantle = Material(
    conductivity = u(3.138,"W/m/K"),
    specific_heat = u(1171,"J/kg/K"),
    density = u(3330,"kg/m**3"))

def test_gdh_temperature():
    assert gdh_temperature(0,0) == 0

    layer = gdh_mantle.to_layer(u(100,'km'))
    solver = GDHSolver(layer)

    for time,depth in [(0,0),(20,50),(10,2)]:
        v1 = gdh_temperature(time,depth)
        v2 = solver._temperature(
            u(time,'Myr'), u(depth,'km'))
        assert v1 == v2

