from __future__ import division
from uncertainties import ufloat as u
from uncertainties.umath import log
from ..microprobe.group import get_cations

class Ca_Olivine(object):
    """From Kohler and Brey, 1990"""
    name = "Ca in Olivine"
    def __init__(self, ol, cpx, **kwargs):
        self.breakout_errors = kwargs.pop("breakout_errors",False)

        self.cpx = get_cations(cpx, oxygen=6, **kwargs)
        self.ol = get_cations(ol, oxygen=4, **kwargs)

        self.D_Ca = self.ol["Ca"]/self.cpx["Ca"]

    def low_temperature(self, T):
        """Need to implement the high temperature version if we are planning
        to measure rocks above ~1275C
        """
        ans = -T*log(self.D_Ca)-u(5792,493)-u(1.25,0.39)*T
        return ans/u(42.5,2.2)

    def high_temperature(self, T):
        ans = -T*log(self.D_Ca)-u(11982,633)+u(3.61,0.47)*T
        return ans/u(56.2,2.7)

    def pressure(self, T=None):
        if T < 1275:
            return -self.low_temperature(T)/10
        else:
            return -self.high_temperature(T)/10

    __call__ = pressure
