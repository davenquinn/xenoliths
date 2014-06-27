#!/usr/bin/env python
from __future__ import division

from geotherm.units import u
from geotherm.materials import oceanic_mantle, continental_crust
from geotherm.models.geometry import Section, Layer, stack_sections
from geotherm.solvers import HalfSpaceSolver, AdvancedFiniteSolver
from geotherm.plot import Plotter

Layer.defaults["grid_spacing"] = u(100,"m")

# Initialize oceanic crust (analytical)
oceanic = HalfSpaceSolver(oceanic_mantle.to_layer(u(100,"km")))
evolved_oceanic = oceanic.solution(u(30,"Myr"))

# Will put royden solver here.

# Initialize continental crust (analytical)
evolved_forearc = Section([continental_crust.to_layer(u(30,"km"))], uniform_temperature=u(200,"degC"))

# Stack the two of them
final_section = stack_sections(
    evolved_forearc.get_slice(u(0,"km"), u(30,"km")),
    evolved_oceanic)

solver = AdvancedFiniteSolver(
    final_section,
    constraints=tuple(u(i,"degC") for i in (25,1500)))

solution = solver.solve_implicit(
    duration=u(20,"Myr"),
    steps=500,
    plotter=Plotter(range=(0,1500)))

list(solution)

# Run to completion
if __name__ == "__main__":
    from IPython import embed
    embed()
