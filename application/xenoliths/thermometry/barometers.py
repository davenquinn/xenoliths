from __future__ import division,print_function
import numpy as N
from uncertainties import ufloat as u
from uncertainties.umath import log
from ..microprobe.group import get_cations, get_molar, get_oxides

# Create a mapping for the linear
# relationship between TA98 and BKN
ta98 = (950,1050)
bkn = (1000,1090)
def ta98_to_bkn(T):
    c = N.polyfit(ta98,bkn,1)
    return c[1]+c[0]*T
def bkn_to_ta98(T):
    c = N.polyfit(ta98,bkn,1)
    return (T-c[1])/c[0]

class Ca_Olivine(object):
    """From Kohler and Brey, 1990"""
    name = "Ca in Olivine"
    init_pressure_basis = 1.5
    def __init__(self, ol, cpx, thermometer, **kwargs):
        self.uncertainties = kwargs.pop('uncertainties',True)
        self.breakout_errors = kwargs.pop("breakout_errors",False)

        # On by default, but can turn off
        self.calibration_uncertainties = kwargs.pop(
            'calibration_uncertainties', self.uncertainties)
        self.monte_carlo = kwargs.pop('monte_carlo',False)

        if self.monte_carlo:
            kwargs['uncertainties'] = True

        # Not really sure if this should be oxide or molar
        # %wt. They don't really matter too much for cpx
        # it seems.
        self.cpx = get_molar(cpx,oxygen=6,**kwargs)
        self.ol = get_molar(ol,oxygen=4,**kwargs)
        self.thermometer = thermometer
        #Offset to keep within spinel stability field
        # Probably relates to Al-tschermakite
        #self.D_Ca = self.ol["Ca"]/self.cpx["Ca"]#*.988

        # This value comes from O'Reilly testing dataset
        self.D_Ca = self.ol["CaO"]/self.cpx["CaO"]*7/10*.988

        # Set up number of monte carlo replications
        if self.monte_carlo:
            c = self.D_Ca
            self.D_Ca = c.n+N.random.randn(self.monte_carlo)*c.s

    def num(self,*args):
        if self.calibration_uncertainties:
            return u(*args)
        else:
            return args[0]

    def pressure(self, input_pressure=1.5, iterative=True, temp_reproducibility=10):
        T = self.thermometer.temperature(input_pressure)
        # Create an offset to work in TA98 space
        TA98 = self.thermometer.name == 'TA98'
        if TA98:
            T = ta98_to_bkn(T)
        T += 273.15
        if self.monte_carlo:
            T = T.n+N.random.randn(self.monte_carlo)*T.s

        if iterative:
            method = self.__iterative_pressure
        else:
            method = self.__pressure

        P = N.array([method(t,d,input_pressure)
                for t,d in zip(T,self.D_Ca)])
        T -= 273.15
        if TA98:
            T = bkn_to_ta98(T)
        return P, T

    def __pressure(self,T,D_Ca,input_pressure):
        first_term = -T*N.log(D_Ca)
        if T <= 1275.25 + 2.827*input_pressure*10:
            ans = first_term-self.num(5792,493)-self.num(1.25,0.39)*T
            P = ans/self.num(42.5,2.2)
        else:
            ans = first_term-self.num(11982,633)+self.num(3.61,0.47)*T
            P = ans/self.num(56.2,2.7)
        return P/10

    # from superclass
    _pressure = __pressure

    def __iterative_pressure(self, T, D_Ca, input_pressure):
        oldPressure = input_pressure
        newPressure = 0
        i = 0
        while i < 500:
            newPressure = self.__pressure(T,D_Ca,oldPressure)
            if N.abs(newPressure - oldPressure) > 0.001:
                oldPressure = newPressure
            else:
                break
            i+=1
        return newPressure

    __call__ = pressure
