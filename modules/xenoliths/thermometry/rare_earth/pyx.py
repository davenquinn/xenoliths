from __future__ import division
from collections import namedtuple
from ..thermometers import TwoPyroxeneThermometer

import numpy as N

class Site(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.keys = entries.keys()
    def values(self):
        return [getattr(self,i) for i in self.keys]
    def as_dict(self):
        return {k: getattr(self,i) for i in self.keys}

class PyroxeneData(object):
    def __init__(self, **data):
        self.__dict__.update(data)

def pyroxene_form(cations):

    get = lambda k: cations.get(k,float("NaN"))

    four = Site(
        Si=get("Si"),
        Al=0,Ti=0)

    six = Site(
        Cr=get("Cr"),
        Al=0,Ti=0,Mg=0,Fe=0)
    # Assign cations to different sites in pyroxene
    Ti = get("Ti")
    Al = get("Al")
    Mg = get("Mg")
    Fe = get("Fe")

    m2 = Site(
        Mn=get("Mn"),
        Ca=get("Ca"),
        Na=get("Na"),
        Ni=get("Ni"), #Nickel has a +3 charge that makes it hard to deal with. Ignoring.
        K=get("K"),
        Fe=0,
        Mg=0)
    # T = Si-Al-Ti

    if four.Si < 2 and Al > 2 - four.Si:
        four.Al = 2 - four.Si
        six.Al = Al - four.Al
    elif Al <= 2 - four.Si:
        four.Al = Al
        if Ti > 2-four.Si - Al:
            four.Ti = 2 - four.Si - Al
            six.Ti = Ti - four.Ti

    Mg_number = Mg/(Mg + Fe)
    M2_t = N.nansum(m2.values()) # ignore nickel

    if Mg > 0:
        R_Fe_Mg = Fe / Mg
        if M2_t <= 1:
            m2.Mg = (1 - M2_t) / (1 + R_Fe_Mg)
            m2.Fe = m2.Mg * R_Fe_Mg

        six.Mg = Mg - m2.Mg
        six.Fe = Fe - m2.Fe
    elif Mg == 0:
        m2.Fe = 1 - M2_t
        six.Fe = Fe - m2.Fe
    return PyroxeneData(
        four=four,
        six=six,
        m2=m2,
        mg_number=Mg_number)

class BKN(TwoPyroxeneThermometer):
    name = "T_BKN (Sun and Liang, 2013 implementation)"
    def __init__(self,*args,**kwargs):
        TwoPyroxeneThermometer.__init__(self,*args,**kwargs)
        self.opx = pyroxene_form(self.formula["opx"])
        self.cpx = pyroxene_form(self.formula["cpx"])

    def temperature(self, pressure=None):
        if pressure is None: pressure = self.P
        pressure *= 10 # BKN uses kilobars internally
        FeN_c = 1 - self.cpx.mg_number
        FeN_o = 1 - self.opx.mg_number
        KD = (1 - self.cpx.m2.Ca / (1 - self.cpx.m2.Na)) / (1 - self.opx.m2.Ca / (1 - self.opx.m2.Na))
        return (23664 + (24.9 + 126.3 * FeN_c) * pressure) / (13.38 + N.log(KD)**2 + 11.59 * FeN_o)-273.15
