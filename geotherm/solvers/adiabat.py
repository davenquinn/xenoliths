from __future__ import division

import numpy as N
from ..units import u

g = u(9.8,"m/s^2")

class AdiabatSolver(object):
    defaults = dict(
        start_temp=u(1300,"degC"),
        start_depth=u(0,"m")
    )
    def __init__(self, **kwargs):
        for k,v in self.defaults.items():
            setattr(self,k,kwargs.pop(k,v))

    def __call__(self, section, **kwargs):
        """
        Iteratively applies adiabatic profile.
        Ignores changing gravity with depth.
        """
        T = self.start_temp.to("K")

        idx = section.cell_centers >= self.start_depth

        # Cell sizes in center of cell
        s = section.cell_centers[idx].into("m")
        s1 = N.roll(s,1)
        s1[0] = self.start_depth.into("m")
        dz = u(s-s1,"m")

        a = section.material_property("thermal_expansivity")[idx]
        Cp = section.material_property("specific_heat")[idx]

        coeff = a*g*dz/Cp
        section.profile[idx] = u(N.cumsum(coeff),"K") + T

        return section

