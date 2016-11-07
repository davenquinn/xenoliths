from __future__ import division, print_function
import numpy as N
from ..units import u
from .finite import AdvancedFiniteSolver as FiniteSolver
from .oceanic import HalfSpaceSolver, GDHSolver
from .forearc import RoydenModel as RoydenSolver
from .adiabat import AdiabatSolver

def steady_state(section, surface_heatflow, surface_temperature=None):
    """
    Iterative solver for steady-state geotherm
    """

    if surface_temperature is None:
        surface_temperature = u(0,'degC')

    ix = 0
    q_top = surface_heatflow
    T_top = surface_temperature.to("K")
    z0 = u(0,'m')
    for layer in section.layers:
        rho = layer.material_property('density')
        a = layer.material_property('heat_generation')
        k = layer.material_property('conductivity')

        T = lambda y: T_top + (q_top-a*y)*y/k + a*y**2/(2*k)

        n = layer.n_cells
        section.profile[ix:ix+n] = T(layer.cell_centers)

        # Radiogenic heat of layer
        z = layer.thickness
        T_top = T(z)
        q_top -= a*z
        z0 += z
        ix += n

    section.profile.to('degC')

    return section
