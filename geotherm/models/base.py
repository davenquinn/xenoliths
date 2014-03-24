from __future__ import division
from ..units import quantity, ensure_unit

class BaseModel(object):
    defaults = {}
    def __init__(self,**kwargs):
        for key,item in self.defaults.items():
            i = quantity(kwargs.get(key,item[0]),item[1])
            setattr(self, key, i)

class MaterialModel(BaseModel):
    defaults = {
        "conductivity": (3.35,"W/m/K"),
        "specific_heat": (1171,"J/K/kg"),
        "density": (3000,"kg/m**3")
    }
    def __init__(self,**kwargs):
        super(MaterialModel, self).__init__(**kwargs)

    @property
    def diffusivity(self):
        a = self.conductivity/self.specific_heat/self.density
        return a.to("m**2/s")

    def length_scale(self, time):
        """
        The distance over which heat will propagate in a given time period.
        Accepts time in seconds
        """
        return N.sqrt(self.diffusivity*ensure_unit(time,u.second))

    def time_scale(self, distance=1000):
        """
        The time over which temperature changes will propagate a given distance.
        Accepts distance in meters (default 1km)
        """
        return (ensure_unit(distance,u.meter)**2/self.diffusivity)
