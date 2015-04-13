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

        # Cell sizes in center of cell
        s = section.cell_sizes.into("m")
        s1 = N.roll(s,1)
        s1[0] = 0
        depth_shift = u(s-s1,"m")

        cells = zip(section.cell_centers, depth_shift)
        for i,(z,dz) in enumerate(cells):
            if z <= self.start_depth:
                continue

            mat = section.material(z)
            a = mat.thermal_expansivity
            c = mat.specific_heat
            dTdz = T*a*g/c
            T += dTdz * dz
            section.profile[i] = T

        return section

