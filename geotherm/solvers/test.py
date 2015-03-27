from __future__ import division, print_function

import numpy as N

from . import HalfSpaceSolver, FiniteSolver
from ..models import Section, Material
from ..units import u

def test_half_space():
    """ Test that the finite element model approaches parity
        with a simple half-space model.
    """
    # We define an oceanic mantle without
    # radiogenic heat generation
    oceanic_mantle = Material(
        conductivity = u(3.35,"W/m"),
        specific_heat = u(1171,"J/kg"),
        density = u(3300,"kg/m**3"))

    t = u(50,"Myr")

    layer = oceanic_mantle.to_layer(u(100,"km"))
    section = Section([layer], uniform_temperature=u(1500,"degC"))
    half_space = HalfSpaceSolver(section)

    finite = FiniteSolver(section)
    sol = finite.solution(t, steps=500)
    hsol = half_space.solution(t)

    print("Maximum error: ",abs(sol-hsol.profile).max())
    assert N.allclose(sol, hsol.profile, atol=10)
