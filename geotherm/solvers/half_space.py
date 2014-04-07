from __future__ import division, print_function
from scipy.special import erf,erfc, erfcinv
from .base import BaseSolver
from ..models.geometry import Section, Layer
from ..units import ensure_unit, unit, u

class HalfSpaceSolver(BaseSolver):
    def __init__(self, layer, **kwargs):
        super(HalfSpaceSolver, self).__init__(**kwargs)
        self.layer = layer
        self.material = layer.material

    def temperature(self,time,depth):
        time = ensure_unit(time, unit.seconds)
        depth = ensure_unit(depth, unit.meters)
        t = self._temperature(time,depth)
        return t.to(unit.degC)

    def _temperature(self,time,depth):
        d = 2*self.material.length_scale(time)
        d = d.into("m")
        first = erfc(depth/d)
        res = first*(self.T_surface.into("K")-self.T_max.into("K"))+self.T_max.into("K")
        return u(res,"K").to("degC")

    def depth(self,time,temperature):
        temp = ensure_unit(temperature, unit.degC)
        theta = (temp-self.T_max).into("K")/(self.T_surface-self.T_max).into("K")
        eta = erfcinv(theta.into("dimensionless"))
        return 2*eta*self.material.length_scale(time)

    def lithospheric_thickness(self,time):
        return self.depth(time,self.T_lithosphere)

    def solution(self,time):
        res = Section([Layer(self.layer.material, self.layer.thickness)])
        res.profile = self._temperature(time,self.layer.cell_centers)
        return res
