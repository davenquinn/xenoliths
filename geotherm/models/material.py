from __future__ import division
from ..units import ensure_unit, unit, u
from .base import BaseModel
from .geometry import Layer
import numpy as N

class Material(BaseModel):
    defaults = dict(
        conductivity = u(3.35,"W/m"),
        specific_heat = u(1171,"J/kg"),
        density = u(3000,"kg/m**3"))

    def __init__(self,**kwargs):
        super(Material, self).__init__(**kwargs)

    @property
    def diffusivity(self):
        a = self.conductivity/self.specific_heat/self.density
        return a.to("m**2/s")

    def length_scale(self, time):
        """
        The distance over which heat will propagate in a given time period.
        
        :arg time: Time in seconds
        """
        return N.sqrt(self.diffusivity*time).to("meters")

    def time_scale(self, distance=u(1,"km")):
        """
        The time over which temperature changes will propagate a given distance.
        Accepts distance in meters (default 1km).
        """
        return distance**2/self.diffusivity

    def to_layer(self, thickness):
        """Returns a Layer object that has a thickness assigned"""
        return Layer(self,thickness)
