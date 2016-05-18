from __future__ import division,print_function
import numpy as N
from uncertainties import ufloat as u
from uncertainties.umath import log
from ..microprobe.group import get_cations, get_molar

class Ca_Olivine(object):
    """From Kohler and Brey, 1990"""
    name = "Ca in Olivine"
    init_pressure_basis = 1.5
    def __init__(self, ol, cpx, thermometer, **kwargs):
        self.uncertainties = kwargs.pop('uncertainties',True)
        self.breakout_errors = kwargs.pop("breakout_errors",False)

        self.monte_carlo = kwargs.pop('monte_carlo',False)

        if self.monte_carlo:
            kwargs['uncertainties'] = True

        self.cpx = get_cations(cpx,oxygen=6,**kwargs)
        self.ol = get_cations(ol,oxygen=4,**kwargs)
        self.thermometer = thermometer
        self.D_Ca = self.ol["Ca"]/self.cpx["Ca"]

        # Set up number of monte carlo replications
        if self.monte_carlo:
            c = self.D_Ca
            self.D_Ca = c.n+N.random.randn(self.monte_carlo)*c.s

    def num(self,*args):
        if self.uncertainties:
            return u(*args)
        else:
            return args[0]

    def pressure(self, input_pressure=2):
        T = self.thermometer.temperature(input_pressure)+273.15
        if self.monte_carlo:
            T = T.n+N.random.randn(self.monte_carlo)*T.s
        P = N.array([self.__pressure(t,d,input_pressure)
                for t,d in zip(T,self.D_Ca)])
        return P, T-273.15

    def __pressure(self,T,D_Ca,input_pressure):
        first_term = -T*N.log(D_Ca)
        if T <= 1275.25 + 2.827*input_pressure*10:
            ans = first_term-self.num(5792,493)-self.num(1.25,0.39)*T
            P = ans/self.num(42.5,2.2)
        else:
            ans = first_term-self.num(11982,633)+self.num(3.61,0.47)*T
            P = ans/self.num(56.2,2.7)
        return P/10

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
