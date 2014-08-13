from __future__ import division, print_function
from scipy.special import erf,erfc, erfcinv
from .base import BaseSolver
from ..models.geometry import Section, Layer
from ..units import ensure_unit, unit, u

class HalfSpaceSolver(BaseSolver):
    """This class implements the Half-space cooling model for cooling oceanic crust."""
    def __init__(self, section, **kwargs):
        super(HalfSpaceSolver, self).__init__(**kwargs)
        self.section = section
        try:
            layers = section.layers
            assert len(layers) == 1
            self.layer = layers[0]
        except AssertionError:
            s = "{0} can be initialized only from a single layer or a section containing only one layer."
            raise ArgumentError(s.format(self.__class__))
        except AttributeError:
            self.layer = layer
        self.material = self.layer.material

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
        res.profile = self.profile(time)
        return res

    def profile(self,time):
        return self._temperature(time,self.section.cell_centers)
