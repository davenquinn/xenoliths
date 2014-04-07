#!/usr/bin/env python
from __future__ import division

from geotherm.units import u
from geotherm.models.material import Material
from geotherm.models.geometry import Layer, Section, stack_sections
from geotherm.solvers import HalfSpaceSolver

oceanic_crust = Material()
continental_crust = Material()

# Initialize oceanic crust (analytical)
oceanic = HalfSpaceSolver(Layer(oceanic_crust, u(100,"km")))
evolved_oceanic = oceanic.solution(u(30,"Myr"))

# Will put royden solver here.

# Initialize continental crust (analytical)
evolved_forearc = Section([Layer(continental_crust, u(30,"km"))], uniform_temperature=u(200,"degC"))

# Stack the two of them
final_section = stack_sections(
    evolved_forearc.get_slice(u(0,"km"), u(30,"km")),
    evolved_oceanic.get_slice(u(0,"km"),u(70,"km"))
    )

# Run to completion
if __name__ == "__main__":
    from IPython import embed
    embed()
