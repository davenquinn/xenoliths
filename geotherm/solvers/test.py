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

    layer = oceanic_mantle.to_layer(u(200,"km"))
    section = Section([layer], uniform_temperature=u(1500,"degC"))
    half_space = HalfSpaceSolver(section)

    c = (u(25,"degC"),u(1500,"degC"))
    finite = FiniteSolver(section, constraints=c)
    sol = finite(t, steps=500)
    hsol = half_space(t)

    f,h = tuple(i.profile for i in (sol, hsol))

    print("Maximum error: ",abs(f-h).max())
    assert N.allclose(f, h, atol=10)

def test_radiogenic_heat():
    """
    Test that the finite element model at steady state
    properly accounts for added heat from radiogenic heating
    """
    pass
