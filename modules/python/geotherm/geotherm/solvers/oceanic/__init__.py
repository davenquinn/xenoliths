

import numpy as N
from scipy.special import erf,erfc, erfcinv

from ..base import BaseSolver
from ..adiabat import AdiabatSolver
from ...models.geometry import Section, Layer
from ...units import ensure_unit, unit, u

class OceanicSolver(BaseSolver):
    def __init__(self, section, **kwargs):
        super(OceanicSolver, self).__init__(**kwargs)
        self.section = section
        if not hasattr(section,"layers"):
            # We need to convert a layer to section
            self.section = Section(self.section)

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
        return t

    def __call__(self,time):
        res = Section([Layer(self.layer.material, self.layer.thickness)])
        res.profile = self.profile(time)
        return res

    def profile(self,time):
        return self._temperature(time,self.section.cell_centers)

class HalfSpaceSolver(OceanicSolver):
    """This class implements the Half-space cooling model for cooling oceanic crust."""
    defaults = dict(
        T_surface=u(0,'degC'),
        T_max=u(1450,'degC'))

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

class GDHSolver(OceanicSolver):
    defaults = dict(
        T_max=u(1450,'degC'),
        lithosphere_depth=u(95,'km'))
    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order',50)
        OceanicSolver.__init__(self, *args,**kwargs)

    def _temperature(self, time, depth):
        """
        An implementation of the "Global Depth and Heat" model of oceanic
        lithosphere cooling from Stein and Stein [1992]. This is elaborated
        in Fowler, Solid Earth, pp294-295

        This is a plate cooling model for oceanic lithosphere (lithosphere is of constant thickness)
        The base of the lithosphere is held at constant temperature T.

        The GDH model tends to have thinner plate and higher temperatures than other models.
        """
        coeff = (depth/self.lithosphere_depth)
        # Prepare Taylor expansion
        n = N.arange(self.order)+1
        try:
            # Expand number of dimensions to
            # match input array of depths
            depth = depth[:,N.newaxis]
            for i in range(depth.ndim-n.ndim):
                n = n[N.newaxis,:]
            n = N.tile(n,depth.shape)
        except IndexError:
            pass
        except TypeError:
            pass
        a = n*N.pi
        aL = (a/self.lithosphere_depth)
        exp = -(aL**2)*self.material.diffusivity*time
        taylor_expansion = 2/a *N.sin(aL*depth) * N.exp(exp)
        coeff += N.sum(taylor_expansion, axis=n.ndim-1)
        coeff = coeff.into('dimensionless')
        return u(self.T_max.into('degC') * coeff,'degC')

    def profile(self,time):
        c = self.section.cell_centers
        profile = self.section.profile.to('degC')

        idx = c < self.lithosphere_depth
        T = self._temperature(time,c[idx])
        profile[idx] = T
        self.section.profile = profile

        adiabat = AdiabatSolver(
            self.section,
            start_depth=self.lithosphere_depth,
            start_temp=self.T_max)

        self.section = adiabat()
        return self.section.profile
