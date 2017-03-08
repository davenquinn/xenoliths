from __future__ import division
from os import path
import numpy as N

from .barometers import Ca_Olivine

class TestBarometer(Ca_Olivine):
    uncertainties=False
    breakout_errors=False
    calibration_uncertainties=False
    monte_carlo=False
    def __init__(self, data):
        # This conforms to O'Reilly testing data at least.
        self.D_Ca = data['Ol_CaO']/data["Cpx_CaO"]*7/10*.988
        print self.D_Ca,data["D"]
        assert N.allclose(self.D_Ca,data["D"], rtol=0.03)
        self.T = data["T"]+273.15
        self.P = data["P"]

    def pressure(self, input_pressure=1.5):
        return self._pressure(self.T,self.D_Ca,input_pressure)

def get_data():
    keys = ("Cpx_CaO","Ol_CaO","D","T","P")
    here = path.dirname(__file__)
    fn = path.join(here,'barometry-test-data.txt')
    with open(fn) as f:
        for line in f:
            if line.startswith("#"):
                continue
            d = line.strip().split()
            if not len(d): continue
            yield {k:float(v) for k,v in zip(keys,d)}

def ca_olivine(data):
    """
    Run a single measurement
    """
    b = TestBarometer(data)
    p = data["P"]/10
    P = b.pressure()
    assert N.allclose(P,p,rtol=.05)

def test_ca_ol():
    """
    Tests the Ca-Olivine barometer with data
    from O'Reilly et al. 1997
    """
    for case in get_data():
        ca_olivine(case)
