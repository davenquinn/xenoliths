from __future__ import division
from uncertainties import ufloat
from uncertainties.umath import log
from functools import partial
from ..models import ProbeMeasurement
from ..microprobe.group import get_cations as get_cations_base

def get_cations(qs,**kwargs):
    try:
        qs['Si']
    except TypeError:
        qs = get_cations_base(qs,**kwargs)
    return qs

class Thermometer(object):
    def __init__(self):
        pass

class TwoPyroxeneThermometer(Thermometer):
    def __init__(self, opx, cpx, **kwargs):
        """
        :param pressure: Pressure in GPa
        :param uncertainties: Whether to use uncertainties in calculation
        """
        self.P = kwargs.pop("pressure", 1.5) #GPa
        self.uncertainties = kwargs.pop("uncertainties",False)
        cations = partial(get_cations,oxygen=6,uncertainties=self.uncertainties)
        self.formula = dict(
            opx=cations(opx),
            cpx=cations(cpx))

class Ca_OPX(Thermometer):
    name = "Ca in OPX"
    def __init__(self, opx, cpx=None, **kwargs):
        """
        :param pressure: Pressure in GPa
        :param uncertainties: Whether to use uncertainties in calculation
        """
        self.P = kwargs.pop("pressure", 1.5) #GPa
        self.opx = get_cations(opx, oxygen=6, **kwargs)

    def temperature(self, pressure=None):
        if pressure == None: pressure = self.P
        pressure = pressure * 10

        top = 6425+26.4*pressure
        bottom = -log(self.opx["Ca"])+1.843
        return top/bottom-273.15

class Ca_OPX_Corr(Ca_OPX):
    """A correction to the Ca-in-OPX thermometer proposed by Nimis and Grutter, 2010"""
    def __init__(self, *args, **kwargs):
        super(Ca_OPX_Corr,self).__init__(*args, **kwargs)
    def temperature(self, pressure=None):
        Tor = super(Ca_OPX_Corr,self).temperature(pressure)
        return -628.7 + 2.0690*Tor - 4.530e-4 * Tor**2


class BKN(TwoPyroxeneThermometer):
    name = "T_BKN"
    def __init__(self, *args, **kwargs):
        super(BKN, self).__init__(*args,**kwargs)

    def X_Fe(self, mineral):
        """Activity of iron"""
        f = self.formula[mineral]
        return f["Fe"]/(f["Fe"]+f["Mg"])

    def Ca_(self, mineral):
        """Calcium and Sodium here are only for the M2 sites supposedly"""
        f = self.formula[mineral]
        return f["Ca"]/(1-f["Na"])

    def temperature(self, pressure=None):
        if pressure == None: pressure = self.P
        pressure = pressure * 10 # BKN uses kilobars internally

        lnKd = log(1-self.Ca_("cpx"))-log(1-self.Ca_("opx"))

        top = 23664+(24.9+126.3*self.X_Fe("cpx"))*pressure
        bottom = 13.38+lnKd**2+11.59*self.X_Fe("opx")
        return top/bottom-273.15

class Taylor1998(TwoPyroxeneThermometer):
    name = "TA98"

    # The Taylor 1998 thermometer reports calibration errors for each
    # of the coefficients used in their formulation of the pyroxene
    # system, based calibration with their empirical results. Including
    # these in the error analysis may be desirable, but they are disabled
    # by default for consistency with other thermometers.
    calibration_errors = False

    def __init__(self, *args, **kwargs):
        self.breakout_errors = kwargs.pop("breakout_errors", False)
        super(Taylor1998, self).__init__(*args,**kwargs)

    def Al_octahedral(self, type):
        f = self.formula[type]
        return f["Al"]/2-f["Cr"]/2-f["Ti"]+f["Na"]/2

    def Al_tetrahedral(self, type):
        f = self.formula[type]
        return f["Al"]/2+f["Cr"]/2+f["Ti"]-f["Na"]/2

    def X_ts(self):
        """
        A correction for tschermak substitution
        (3+ cation in both octahedral and tetrahedral site)
        Ex. Ca Al2 Si O6 (don't know if that actually happens)
        """
        f = self.formula["cpx"]
        return f["Al"]+f["Cr"]-f["Na"]

    def a_en(self, type):
        "A term for the activity of enstatite"
        f = self.formula[type]
        a = 1-f["Ca"]-f["Na"]
        b = 1-self.Al_octahedral(type)-f["Cr"]-f["Ti"]
        c = (1-self.Al_tetrahedral(type)/2)**2
        activity = a*b*c
        return activity

    def num(self,num,unc,idx=0):
        if not self.uncertainties:
            return num
        if not self.calibration_errors:
            return num
        if not self.breakout_errors: idx = ""
        return ufloat(num,unc,"th"+str(idx))

    def temperature(self, pressure=None):
        """Uncertainties from Taylor, page 402"""
        if pressure == None: pressure = self.P
        cpx = self.formula["cpx"]
        opx = self.formula["opx"]

        lnKd = log(self.a_en("cpx"))-log(self.a_en("opx"))

        bottom = sum([
            self.num(15.67,0.77, "0"),
            self.num(14.37,3.13, "1")*cpx["Ti"],
            self.num(3.69,1.61, "2")*cpx["Fe"],
            self.num(-3.25,0.81, "3")*self.X_ts(),
            lnKd**2
        ])

        T = (self.num(24787,826, "4")+self.num(678,87,"5")*pressure)/bottom
        return T-273.15
