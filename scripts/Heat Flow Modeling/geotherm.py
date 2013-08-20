#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
This file defines a model continental geotherm using methods similar to
Luffi et al, 2009. 
"""

import numpy as N

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
    def __init__(self):
        self.T_0 = 30
        self.q_m = 57 #±3 mW/m2 (Luffi et al.)
        self.q_0 = 95 # Luffi