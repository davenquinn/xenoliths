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
        old_z = u(0,"m")
        for i,z in enumerate(section.cell_centers):
            dz = z-old_z
            old_z = z
            if z <= self.start_depth:
                continue
            section.profile[i] = T

            mat = section.material(z)
            a = mat.thermal_expansivity
            c = mat.specific_heat
            dTdz = T*a*g/c
            T += dTdz * dz

