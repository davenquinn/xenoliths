from __future__ import division, print_function
from ..units import ensure_unit, u
from .base import BaseModel
import numpy as N
from itertools import chain

class Layer(BaseModel):
    defaults = dict(
        grid_spacing = u(10,"m"))
    def __init__(self, material, thickness, **kwargs):
        BaseModel.__init__(self,**kwargs)
        self.material = material
        self.thickness = thickness
        try:
            self.n_cells = (self.thickness/self.grid_spacing).into("dimensionless")
            assert self.n_cells % 1 == 0
            self.n_cells = int(self.n_cells)
        except AssertionError:
            msg = "Layer thickness must be an integer multiple of the grid spacing"
            raise ArgumentError(msg)

        self.cell_boundaries = N.arange(self.n_cells)*self.grid_spacing
        self.cell_centers = self.cell_boundaries+self.grid_spacing/2

class Section(BaseModel):
    """
    A section of crust that contains several layers with individually-defined
    material models. Rudimentary support for unequal grid spacing (defined per-layer)
    """
    thickness = property(lambda self:\
            sum([i.thickness for i in self.layers]))
    n_cells = property(lambda self:\
            sum([i.n_cells for i in self.layers]))
    cell_sizes = property(lambda self:\
            (self.cell_centers - self.cell_boundaries)*2)

    def __init__(self, layers, **kwargs):
        self.layers = layers
        self.profile = kwargs.pop("profile", None)
        uniform_temperature = kwargs.pop("uniform_temperature", u(0,"degC"))
        if self.profile is None:
            self.profile = N.ones(self.n_cells)*uniform_temperature.to("K")

    @property
    def cell_boundaries(self):
        func = lambda layer, offset: (layer.cell_boundaries+offset).into("meters")
        ls = [func(layer,top) for (top,bottom), layer in self.iterlayers()]
        return u(N.concatenate(ls),"m")

    @property
    def cell_centers(self):
        func = lambda layer, offset: (layer.cell_centers+offset).into("meters")
        ls = [func(layer,top) for (top,bottom), layer in self.iterlayers()]
        return u(N.concatenate(ls),"m")

    def iterlayers(self):
        top = u(0,"km")
        for layer in self.layers:
            bottom = top+layer.thickness
            yield (top,bottom), layer
            top = bottom

    def material_property(self, parameter):
        """ Returns an array of a material parameter (such as
            diffusivity, density)
        """
        i = 0
        arr = N.empty(self.n_cells)
        for layer in self.layers:
            coeff = getattr(layer.material, parameter)
            arr[i:i+layer.n_cells] = coeff
            i += layer.n_cells
        return u(arr,coeff.units)

    def layer_bounds(self):
        return N.concatenate(list(self.iterlayers()))

    def material(self,depth):
        for (top,bottom),layer in self.iterlayers():
            if top < depth < bottom:
                return layer.material
        return None

    def depth(self, temperature):
        """
        Minimum depth where a certain temperature is exceeded.
        """
        test = self.profile > temperature
        return self.cell_centers[test][0]

    def get_slice(self, top, bottom):
        def layers():
            for bounds, layer in self.iterlayers():
                thickness = layer.thickness
                if bounds[0] >= bottom or bounds[1] <= top: continue
                if bounds[0] < top:
                    thickness -= (top-bounds[0])
                if bounds[1] > bottom:
                    thickness -= (bounds[1]-bottom)
                yield Layer(layer.material, thickness)

        a = Section(list(layers()))
        mask = N.logical_and(top < self.cell_centers, self.cell_centers < bottom)
        a.profile = self.profile[mask]
        return a

def stack_sections(*args):
    """Stack a list of sections to form an aggregate."""
    layers = list(chain.from_iterable((sect.layers for sect in args)))
    a = Section(layers)
    profiles = list(sect.profile.into("degC") for sect in args)
    a.profile = u(N.concatenate(profiles),"degC")
    return a
