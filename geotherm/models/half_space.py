from __future__ import division
from scipy.special import erf,erfc, erfcinv
from .base import BaseModel
from ..units import quantity, ensure_unit, registry

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
        time = ensure_unit(time, registry.seconds)
        depth = ensure_unit(depth, registry.meters)
        t = self._temperature(time,depth)
        return t.to(registry.degC)

    def _temperature(self,time,depth):
        d = self.material.length_scale(time).magnitude
        first = erfc(depth/(2*d))
        return first*(self.T_surface.magnitude-self.T_max.magnitude)+self.T_max.to("kelvin").magnitude

    def depth(self,time,temperature):
        temp = ensure_unit(temperature, registry.degC)
        theta = (temp-self.T_max).magnitude/(self.T_surface-self.T_max).magnitude
        eta = erfcinv(theta)
        return 2*eta*self.material.length_scale(time)

    def lithospheric_thickness(self,time):
        return self.depth(time,self.T_lithosphere)
