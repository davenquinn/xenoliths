from __future__ import division
from ..units import ensure_unit, unit, u
from .base import BaseModel
import numpy as N

class Material(BaseModel):
    defaults = {
        "conductivity": u(3.35,"W/m/K"),
        "specific_heat": u(1171,"J/K/kg"),
        "density": u(3000,"kg/m**3")
    }
    def __init__(self,**kwargs):
        super(Material, self).__init__(**kwargs)

    @property
    def diffusivity(self):
        a = self.conductivity/self.specific_heat/self.density
        return a.to("m**2/s")

    def length_scale(self, time):
        """
        The distance over which heat will propagate in a given time period.
        Accepts time in seconds
        """
        return N.sqrt(self.diffusivity*time).to("meters")

    def time_scale(self, distance=u(1,"km")):
        """
        The time over which temperature changes will propagate a given distance.
        Accepts distance in meters (default 1km)
        """
        return distance**2/self.diffusivity
