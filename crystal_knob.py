#!/usr/bin/env python
"""
Solver for geothermal models related to the Crystal Knob xenoliths

Usage: crystal_knob.py <solution>
"""
from __future__ import division, print_function
from docopt import docopt
import json
from geotherm.plot import Plotter
from geotherm.units import u
from geotherm.materials import oceanic_mantle, continental_crust
from geotherm.models.geometry import Section, Layer, stack_sections
from geotherm.solvers import HalfSpaceSolver
from geotherm.solvers.finite import AdvancedFiniteSolver

args = docopt(__doc__)
solution = args["<solution>"]

plotter = Plotter(range=(0,1500))


present = u(1.65,"Myr") # K-Ar age for Crystal Knob xenoliths


solver_constraints = (
    u(25,"degC"), # Surface temperature
    u(1500,"degC"))
    #u(48,"mW/m**2"))
    # Globally averaged mantle heat flux from Pollack, et al., 1977

oceanic_section = Section([oceanic_mantle.to_layer(u(100,"km"))])
oceanic_solver = HalfSpaceSolver(oceanic_section)

forearc = Section([
    continental_crust.to_layer(u(30,"km"))
    ], uniform_temperature=u(400,"degC")) # This is obviously over-simplified

def basic_case(start, subduction):
    """Both the Monterey and Farallon-Plate scenarios involve the same
    basic steps, just with different timing.
    """
    underplated_oceanic = oceanic_solver.solution(start-subduction)

    final_section = stack_sections(
        forearc,
        underplated_oceanic)

    solver = AdvancedFiniteSolver(
        final_section,
        constraints=solver_constraints)

    return solver.solution(
        subduction-present,
        steps=500,
        plotter=plotter)

def monterey_plate():
    print("Monterey Plate")
    start = u(28,"Myr")
    subduction = u(26,"Myr")
    return basic_case(start,subduction)

def farallon_plate():
    print("Farallon Plate")
    start = u(140, "Myr")
    subduction = u(70, "Myr")
    return basic_case(start,subduction)

def underplating():
    print("Underplating")
    start = u(20,"Myr")

    slab_window_upwelling = Section([
        oceanic_mantle.to_layer(u(100,"km"))
    ], uniform_temperature=u(1300,"degC"))

    final_section = stack_sections(
        forearc,
        slab_window_upwelling)

    solver = AdvancedFiniteSolver(
        final_section,
        constraints=solver_constraints)

    return solver.solution(
        duration=start-present,
        steps=200,
        plotter=plotter)


if solution == "monterey":
    monterey = monterey_plate()


if solution == "farallon":
    farallon = farallon_plate()

if solution == "underplating":
    underplating = underplating()

if solution == "everything":
    data = dict(
        monterey=list(monterey_plate().into("degC")),
        farallon=list(farallon_plate().into("degC")),
        underplating=list(underplating().into("degC"))
    )
    with open("data/models.json", "w") as f:
        json.dump(data, f)
