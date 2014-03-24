from __future__ import division
from scipy.special import erf,erfc, erfcinv
from .base import BaseModel
from ..units import quantity, ensure_unit

class HalfSpace(BaseModel):
    defaults = {
        "T_surface": (25,"degC"),
        "T_max": (1500,"degC"),
        "T_lithosphere": (1300,"degC")
    }
    def __init__(self, material_model, **kwargs):
        super(HalfSpace, self).__init__(**kwargs)
        self.material = material_model

    def temperature(self,time,depth):
        time = ensure_unit(time, u.seconds)
        depth = ensure_unit(depth, u.meters)
        d = self.material.length_scale(time)
        t = erfc(float(depth/(2*d)))*(self.T_max-self.T_surface)+self.T_surface
        return t.to(u.degC)

    def depth(self,time,temperature):
        temp = ensure_unit(temperature, u.degC)
        theta = (temp-self.T_max).magnitude/(self.T_surface-self.T_max).magnitude
        eta = erfcinv(theta)
        return 2*eta*self.material.length_scale(time)

    def lithospheric_thickness(self,time):
        return self.depth(time,self.T_lithosphere)
