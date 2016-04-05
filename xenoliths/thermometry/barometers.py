from __future__ import division
import numpy as N
from uncertainties import ufloat as u
from uncertainties.umath import log
from ..microprobe.group import get_molar

class Ca_Olivine(object):
    """From Kohler and Brey, 1990"""
    name = "Ca in Olivine"
    init_pressure_basis = 1.5
    def __init__(self, ol, cpx, thermometer, **kwargs):
        self.uncertainties = kwargs.pop('uncertainties',True)
        self.breakout_errors = kwargs.pop("breakout_errors",False)

        self.cpx = get_molar(cpx, **kwargs)
        self.ol = get_molar(ol, **kwargs)
        self.thermometer = thermometer
        self.D_Ca = self.ol["CaO"]/self.cpx["CaO"]*7/10

    def num(self,*args):
        if self.uncertainties:
            return u(*args)
        else:
            return args[0]

    def low_temperature(self, T):
        """Need to implement the high temperature version if we are planning
        to measure rocks above ~1275C
        """
        ans = -T*log(self.D_Ca)-self.num(5792,493)-self.num(1.25,0.39)*T
        return ans/self.num(42.5,2.2)

    def high_temperature(self, T):
        ans = -T*log(self.D_Ca)-self.num(11982,633)+self.num(3.61,0.47)*T
        return ans/self.num(56.2,2.7)

    def pressure(self, input_pressure=1.5):
        T = self.thermometer.temperature(input_pressure)+273.15
        return self._pressure(T,input_pressure)

    def _pressure(self,T,input_pressure):
        if T <= 1275.25 + 2.827*input_pressure*10:
            return self.low_temperature(T)/10
        else:
            return self.high_temperature(T)/10

    def iterative_pressure(self):
        oldPressure = self.init_pressure_basis
        newPressure = 0
        i = 0
        while i < 500:
            newPressure = self.pressure(oldPressure)
            if N.abs(newPressure - oldPressure) > 0.001:
                oldPressure = newPressure
            else:
                break
            i+=1
        return newPressure

    __call__ = pressure
