# -*- coding: utf-8 -*-
from __future__ import division
import numpy as N
from itertools import product

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
    K = 8.04732999438e-07

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

# Time, depth grid
def grid():
    src = product(range(0,100,20),range(0,100,20))
    for time, depth in src:
        if time == depth == 0:
            continue
        yield u(time,'Myr'), u(depth,'km')

layer = gdh_mantle.to_layer(u(100,'km'))
gdh_solver = GDHSolver(layer, order=50)
hs_solver = HalfSpaceSolver(layer,
        T_surface=u(0,'degC'),
        T_max=u(1450,'degC'))

def test_gdh_temperature():
    assert gdh_temperature(0,0) == 0

    for time,depth in grid():
        v1 = gdh_temperature(time.into('Myr'),depth.into('km'))
        v2 = gdh_solver.temperature(time,depth).into('degC')
        assert N.allclose(v1,v2, atol=5, rtol=0.05)

def test_array():
    """
    Passing an array of depths to the GDH
    model is tricky due to its Taylor-expansion
    design.
    """
    time = u(20,'Myr')
    depths = u(N.array([10,20]),'km')

    res = gdh_solver.temperature(time,depths)
    for depth,v0 in zip(depths,res):
        v1 = gdh_solver.temperature(time,depth)
        assert N.allclose(v0,v1)

def test_consistency():
    """
    Test the relative consistency of the GDH and
    half-space cooling models. GDH should predict
    higher temperatures, but not inordinately so.
    """
    for time,depth in grid():
        if time.into('s') == 0: continue
        if depth.into('m') == 0: continue
        gdh = gdh_solver.temperature(time,depth)
        hs = hs_solver.temperature(time,depth)
        assert gdh >= hs
        assert N.allclose(gdh,hs,rtol=0.2)



