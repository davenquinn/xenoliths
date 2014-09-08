#!/usr/bin/env python
"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
import json

from functools import partial

from geotherm.units import u
from geotherm.materials import oceanic_mantle, continental_crust, oceanic_crust
from geotherm.models.geometry import Section, Layer, stack_sections
from geotherm.solvers import HalfSpaceSolver, FiniteSolver

from . import results_dir
from ..application import app

present = u(1.65,"Myr") # K-Ar age for Crystal Knob xenoliths

solver_constraints = (
    u(25,"degC"), # Surface temperature
    u(1400,"degC"))
    #u(48,"mW/m**2"))
    # Globally averaged mantle heat flux from Pollack, et al., 1977

oceanic_section = Section([
    oceanic_crust.to_layer(u(10,"km")),
    oceanic_mantle.to_layer(u(270,"km"))],
    uniform_temperature=u(1400,"degC"))
oceanic_solver = FiniteSolver(oceanic_section, constraints=solver_constraints)

forearc = Section([
    continental_crust.to_layer(u(30,"km"))
    ], uniform_temperature=u(400,"degC")) # This is obviously over-simplified

def subduction_case(name, start_time, subduction_time):
    """Both the Monterey and Farallon-Plate scenarios involve the same
    basic steps, just with different timing.
    """
    print(name)
    plot_opts = dict(
        range=(0,1500),
        title=name)

    underplated_oceanic = oceanic_solver.solution(start_time-subduction_time)

    final_section = stack_sections(
        forearc,
        underplated_oceanic)

    solver = FiniteSolver(
        final_section,
        constraints=solver_constraints)

    return solver.solution(
        subduction_time-present,
        steps=500,
        plot_options=plot_opts)

monterey_plate = partial(
    subduction_case,
    "Monterey Plate",
    u(28,"Myr"),
    u(26,"Myr"))

farallon_plate = partial(
    subduction_case,
    "Farallon Plate",
    u(140, "Myr"),
    u(70, "Myr"))

def underplating():
    name = "Underplating"

    start = u(20,"Myr")

    slab_window_upwelling = Section([
        oceanic_mantle.to_layer(u(270,"km"))
    ], uniform_temperature=u(1400,"degC"))
    # This should be a mantle adiabat.

    final_section = stack_sections(
        forearc,
        slab_window_upwelling)

    solver = FiniteSolver(
        final_section,
        constraints=solver_constraints)

    return solver.solution(
        duration=start-present,
        steps=100,
        plot_options=plot_opts)

def solve():
    # This does the computational heavy lifting
    data = dict(
        monterey=list(monterey_plate().into("degC")),
        farallon=list(farallon_plate().into("degC")),
        underplating=list(underplating().into("degC")))
    fn = results_dir("models.json")
    with open(str(fn),"w") as f:
        json.dump(data, f)
