

import numpy as N
from ..units import u
from ..models import Section

# Should update to have a single temperature at the surface.

class AdiabatSolver(object):
    defaults = dict(
        start_temp=u(1300,"degC"),
        start_depth=u(0,"m"))
    def __init__(self, section, **kwargs):

        self.section = section
        if not hasattr(section,"layers"):
            # We need to convert a layer to section
            section = Section(section)

        for k,v in list(self.defaults.items()):
            setattr(self,k,kwargs.pop(k,v))

    @property
    def gradient(self):
        """
        dT/dz for adiabat calculations
        """
        idx = self.section.cell_centers >= self.start_depth
        _ = self.section.material_property

        g = u(10,"m/s^2")
        a = _("thermal_expansivity")
        Cp = _("specific_heat")
        T = u(1350,"degC").to('K')

        return a*g*T/Cp

    def __call__(self, **kwargs):
        """
        Iteratively applies adiabatic profile.
        Ignores changing gravity with depth.

        Values from Turcotte and Schubert, 2002 (p340)
        """

        idx = self.section.cell_centers >= self.start_depth

        # Cell sizes in center of cell
        s = self.section.cell_centers[idx].into("m")
        s1 = N.roll(s,1)
        s1[0] = self.start_depth.into("m")
        dz = u(s-s1,"m")
        coeff = self.gradient[idx]

        coeff *= dz
        integrated = u(N.cumsum(coeff.into('K')),coeff.units)
        _ = integrated.into('K') + self.start_temp.into("K")
        self.section.profile[idx] = u(_,'K').to('degC')

        return self.section
