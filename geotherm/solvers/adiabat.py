from __future__ import division

import numpy as N
from ..units import u

class AdiabatSolver(object):
    defaults = dict(
        start_temp=u(1300,"degC"),
        start_depth=u(0,"m"))
    def __init__(self, **kwargs):
        for k,v in self.defaults.items():
            setattr(self,k,kwargs.pop(k,v))

    def __call__(self, section, **kwargs):
        """
        Iteratively applies adiabatic profile.
        Ignores changing gravity with depth.

        Values from Turcotte and Schubert, 2002 (p340)
        """

        idx = section.cell_centers >= self.start_depth

        # Cell sizes in center of cell
        s = section.cell_centers[idx].into("m")
        s1 = N.roll(s,1)
        s1[0] = self.start_depth.into("m")
        dz = u(s-s1,"m")

        g = u(10,"m/s^2")
        a = section.material_property("thermal_expansivity")[idx]
        Cp = section.material_property("specific_heat")[idx]
        T = u(1450,"degC").to('K')

        coeff = a*g*dz*T/Cp
        integrated = u(N.cumsum(coeff.into('K')),coeff.units)
        _ = integrated.into('K') + self.start_temp.into("K")
        section.profile[idx] = u(_,'K').to('degC')

        return section
