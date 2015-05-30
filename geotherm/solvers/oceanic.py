#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
Here we implement the "Global Depth and Heat" model of oceanic lithosphere cooling from Stein and Stein [1992].
This is elaborated in Fowler, Solid Earth, pp294-295

This is a plate cooling model for oceanic lithosphere (lithosphere is of constant thickness)
Base of lithosphere is held at constant temperature T

GDH model tends to have thinner plate and higher temperatures than other models.

We will use the output of this model at time `n` to seed our underplated lithosphere geotherm models.
"""

from __future__ import division
import numpy as N

class PlateModel(object):
    """
    This is a generic plate model that implements the equations governing the model.
    """
    def __init__(self, variables):
        self.set_vars(variables)

    def set_vars(self,vars):
        self.vars = {}
        for var in vars:
            self.vars[var[0]] = {
                "value": var[1],
                "desc": var[2]
            }
    def get_vars(self, variables):
        return tuple([self.vars[v]["value"] for v in list(variables)])

    def temperature(self, depth, t, order=50):
        """This equation is simplified to ignore horizontal heat conduction"""
        Ta, L, K = self.get_vars(("Ta","L","K"))
        t *= 3.15569e7
        def summation_term(n):
            ex = (n*N.pi/L)**2
            return 2 / (n*N.pi) * N.sin(n*N.pi*depth/L) * N.exp(-ex*K*t)

        taylor_expansion = N.array([summation_term(i+1) for i in range(order)])
        print N.sum(taylor_expansion, axis=0).shape

        sol = Ta * (depth/L + N.sum(taylor_expansion, axis=0))
        print sol.shape
        return sol

    __call__ = temperature

GDH_variables = [
    ("L", 95, "Plate thickness (km)"),
    ("Ta", 1450, "Asthenospheric temperature"),
    ("a", 3.1e-5, "Coefficient of thermal expansion (1/ºC)"),
    ("k", 3.138, "Thermal conductivity (W/m)"),
    ("cp", 1.171, "Specific heat (kJ/kg)"),
    ("K", 0.804e-6, "Thermal diffusivity (m^2/s)"),
    ("pm",3330,"Mantle density (kg/m3)"),
    ("pw",1000,"Water density (kg/m3)"),
    ("dr", 2.6,"Ridge depth (km)")
]

class GDH_Model(PlateModel):
    def __init__(self):
        super(GDH_Model, self).__init__(GDH_variables)



