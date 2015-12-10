from __future__ import division, print_function
from scipy.special import erf,erfc, erfcinv

from ..base import BaseSolver
from ...models.geometry import Section, Layer
from ...units import ensure_unit, unit, u

class OceanicSolver(BaseSolver):
    def __init__(self, section, **kwargs):
        super(OceanicSolver, self).__init__(**kwargs)
        self.section = section
        try:
            layers = section.layers
            assert len(layers) == 1
            self.layer = layers[0]
        except AssertionError:
            s = "{} can be initialized only from a single layer or a section containing only one layer."
            raise ArgumentError(s.format(self.__class__))
        except AttributeError:
            # We were provided with a single homogenous layer
            self.layer = section
        self.material = self.layer.material

    def temperature(self,time,depth):
        time = ensure_unit(time, unit.seconds)
        depth = ensure_unit(depth, unit.meters)
        t = self._temperature(time,depth)
        return t.to(unit.degC)

class HalfSpaceSolver(OceanicSolver):
    """This class implements the Half-space cooling model for cooling oceanic crust."""

    def _temperature(self,time,depth):
        d = 2*self.material.length_scale(time)
        d = d.into("m")
        first = erfc(depth/d)
        res = first*(self.T_surface.into("K")-self.T_max.into("K"))+self.T_max.into("K")
        return u(res,"K").to("degC")

    def depth(self,time,temperature):
        temp = ensure_unit(temperature, unit.degC)
        theta = (temp-self.T_max).to("K")/(self.T_surface-self.T_max).to("K")
        eta = erfcinv(theta.into("dimensionless"))
        return 2*eta*self.material.length_scale(time)

    def lithospheric_thickness(self,time):
        return self.depth(time,self.T_lithosphere)

    def __call__(self,time):
        res = Section([Layer(self.layer.material, self.layer.thickness)])
        res.profile = self.profile(time)
        return res

    def profile(self,time):
        return self._temperature(time,self.section.cell_centers)

class GDHSolver(OceanicSolver):
    def temperature(self, depth, t, order=50):
        """
        An implementation of the "Global Depth and Heat" model of oceanic
        lithosphere cooling from Stein and Stein [1992]. This is elaborated
        in Fowler, Solid Earth, pp294-295

        This is a plate cooling model for oceanic lithosphere (lithosphere is of constant thickness)
        The base of the lithosphere is held at constant temperature T.

        The GDH model tends to have thinner plate and higher temperatures than other models.
        """
        Ta = self.T_max
        Ta, L, K = self.get_vars(("Ta","L","K"))
        t *= 3.15569e7
        def summation_term(n):
            ex = (n*N.pi/L)**2
            return 2 / (n*N.pi) * N.sin(n*N.pi*depth/L) * N.exp(-ex*K*t)

        taylor_expansion = N.array([summation_term(i+1) for i in range(order)])
        print(N.sum(taylor_expansion, axis=0).shape)

        sol = Ta * (depth/L + N.sum(taylor_expansion, axis=0))
        print(sol.shape)
        return sol
