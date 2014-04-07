from __future__ import division
from ..units import ensure_unit, u
from .base import BaseModel
import numpy as N
from itertools import chain
import IPython

class Layer(BaseModel):
    defaults = dict(
        grid_spacing = u(10,"m")
    )
    def __init__(self, material, thickness, **kwargs):
        super(Layer, self).__init__(**kwargs)
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
    """Rudimentary support for unequal grid spacing (defined per-layer)"""
    def __init__(self, layers, **kwargs):
        self.layers = layers
        self.thickness = N.sum([i.thickness for i in self.layers])
        self.n_cells = N.sum([i.n_cells for i in self.layers])
        self.cell_centers = self.set_cell_centers()
        self.cell_boundaries = self.set_cell_boundaries()

        uniform_temperature = kwargs.pop("uniform_temperature", None)
        if uniform_temperature is not None:
            self.profile = N.ones(self.n_cells)*uniform_temperature
        else:
            self.profile = None

    def set_cell_boundaries(self):
        def layers():
            a = u(0,"m")
            for layer in self.layers:
                yield (layer.cell_boundaries + a).into("meters")
                a += layer.thickness
        return u(N.concatenate(list(layers())),"m")

    def set_cell_centers(self):
        def layers():
            a = u(0,"m")
            for layer in self.layers:
                yield (layer.cell_centers + a).into("meters")
                a += layer.thickness
        return u(N.concatenate(list(layers())),"m")

    def layer_bounds(self):
        def accumulate():
            a = u(0,"km")
            for layer in self.layers:
                b = a+layer.thickness
                yield (a,b), layer
                a = b
        return N.concatenate(list(accumulate()))

    def get_slice(self, top, bottom):
        def layers():
            for bounds, layer in zip(self.layer_bounds(),self.layers):
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
    """Append a list of sections to form an aggregate."""
    layers = list(chain.from_iterable((sect.layers for sect in args)))
    a = Section(layers)
    a.profile = u(N.concatenate(list(sect.profile.into("degC") for sect in args)),"degC")
    return a
