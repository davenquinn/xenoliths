#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
This file defines a model continental geotherm using methods similar to
Luffi et al, 2009. 
"""
from __future__ import division
import numpy as N
from scipy.optimize import fsolve

class HeatFlowModel(object):
    """
    Heat flow equations are taken from Turcotte and Schubert, 2002 
    Geodynamics (eqn 4-31, p274)
    T = T_0 + q_m*y/k + (q_0 − q_m)*h_r (1 − exp(−y/h_r )) / k

    q_m: lower boundary condition (heat flux from asthenosphere)
    q_0: upper boundary condition (heat flux at surface)
    T_0: temperature of surface
    h_r: scale height for factor of e decrease in radioactive heat flux
    k: decay constant in heat
    y: depth
    """
    T_0 = 30
    q_m = 57 #±3 mW/m2 (Luffi et al.)
    q_0 = 95 # Luffi, Erkan and Blackwell (estimated from Fig. 1)
    K = 3.35 # W/m/K (Turcotte and Schubert, 2002)
    h_r = 10 #m

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


    def temperature(self, depth):
        return self.T_0 + self.q_m * depth /self.K + (self.q_0 - self.q_m) * self.h_r*(1 - N.exp(- depth/self.h_r)) / self.K

    def get_depth(self, temperature):
        return fsolve(lambda d: self.temperature(d)-temperature, temperature/20.)