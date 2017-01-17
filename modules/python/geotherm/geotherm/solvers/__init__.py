from __future__ import division, print_function
import numpy as N
from ..units import u
from .finite import AdvancedFiniteSolver as FiniteSolver
from .oceanic import HalfSpaceSolver, GDHSolver
from .forearc import RoydenModel as RoydenSolver
from .adiabat import AdiabatSolver

def steady_state(section, surface_heatflow, surface_temperature=None):
    """
    Iterative solver for steady-state geotherm based only on the
    surface heat flux with no assumption on steady-state
    heat flow from mantle (i.e. radiogenic heat generation
    is assumed to be known).
    """
    if surface_temperature is None:
        surface_temperature = u(0,'degC')

    ix = 0
    q_top = surface_heatflow
    T_top = surface_temperature.to("K")
    z0 = u(0,'m')
    for layer in section.layers:
        a = layer.material_property('heat_generation')
        k = layer.material_property('conductivity')

        def temperature(depth):
            T = T_top
            T -= a/(2*k)*depth**2
            T += q_top*depth/k
            return T

        n = layer.n_cells
        section.profile[ix:ix+n] = temperature(layer.cell_centers)

        # Radiogenic heat of layer
        dz = layer.thickness
        T_top = temperature(dz)
        q_top -= a*dz
        z0 += dz
        ix += n

    section.profile.to('degC')

    return section

def steady_state_mantle(section, surface_heatflow,
                         reduced_heatflow=None,
                         surface_temperature=None,
                         characteristic_scale=u(10,'km'),
                         heatflow_mantle_proportion=0.6):
    if surface_temperature is None:
        surface_temperature = u(0,'degC')
    # Use empiricism of Pollack and Chapman, 1977
    # to relate mantle heat flow to surface heat flow
    # if we don't specify a mantle heat flow
    # q* = 0.6 q0
    # This is what Luffi, 2009 did, but more generalized
    if reduced_heatflow is None:
        reduced_heatflow = heatflow_mantle_proportion*surface_heatflow

    # Turcotte and Schubert [2002, equation 4-31]

    # This is what we use for oceanic mantle in our modeling
    k = section.material_property('conductivity')
    z = section.cell_centers

    T = surface_temperature.to('K')
    T += reduced_heatflow*z/k
    _ = surface_heatflow-reduced_heatflow
    T += (_*characteristic_scale/
            k*(1-N.exp(-z/characteristic_scale)))

    lyrs = section.layers
    ix = 0
    for i,layer in enumerate(lyrs):
        if i == len(lyrs)-1:
            continue
        n = layer.n_cells
        # Get difference between adjacent cells and add
        # ... this allows us to not calculate the heat
        # ... flux at every interlayer surface
        ix += n
        dq = T[ix-1]-T[ix]
        T[ix:]+=dq

    section.profile = T.to('degC')

    return section

