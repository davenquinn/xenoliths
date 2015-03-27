"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
import json
from click import echo

from functools import partial

from geotherm.units import u
from geotherm.models.geometry import Section, Layer, stack_sections
from geotherm.solvers import HalfSpaceSolver, FiniteSolver, RoydenSolver
from geotherm.materials import oceanic_mantle, continental_crust

from .scenario import ModelScenario
from .forearc import forearc_section
from . import results_dir

present = u(1.65,"Myr") # K-Ar age for Crystal Knob xenoliths

solver_constraints = (
    u(25,"degC"), # Surface temperature
    u(1500,"degC"))
    #u(48,"mW/m**2"))
    # Globally averaged mantle heat flux from Pollack, et al., 1977

steps = 50

def subduction_case(name, start_time, subduction_time):
    """Both the Monterey and Farallon-Plate scenarios involve the same
    basic steps, just with different timing.
    """
    print(name)

    oceanic = Section([oceanic_mantle.to_layer(u(250,"km"))])

    half_space = HalfSpaceSolver(oceanic)

    t = start_time-subduction_time

    underplated_oceanic = half_space(t)

    T_lithosphere = u(1300,"degC")

    d = half_space.depth(t, T_lithosphere)

    distance = 100e3

    echo("Depth of the base of the "
        "lithosphere at the time of "
        "subduction:{0:.2f}".format(d))

    forearc = forearc_section(
            distance = distance,
            Tm = T_lithosphere.into("degC"),
            l = d.into("m"))

    echo("Temperature at subduction interface "
         "at the time of underplating: {0}"\
          .format(forearc.profile[-1]))

    final_section = stack_sections(
        forearc,
        underplated_oceanic)

    solver = FiniteSolver(
        final_section,
        constraints=solver_constraints)

    return solver(
        subduction_time-present,
        steps=steps)

monterey_plate = partial(
    subduction_case,
    "Monterey Plate",
    u(28,"Myr"),
    u(26,"Myr"))

farallon_plate = partial(
    subduction_case,
    "Farallon Plate")

def underplating():
    name = "Underplating"

    plot_opts = dict(
        range=(0,1500),
        title=name)

    start = u(20,"Myr")

    forearc = Section([continental_crust.to_layer(u(30,"km"))],
            uniform_temperature=u(400,"degC"))

    slab_window_upwelling = Section([
        oceanic_mantle.to_layer(u(270,"km"))
    ], uniform_temperature=u(1500,"degC"))
    # This should be a mantle adiabat.

    final_section = stack_sections(
        forearc,
        slab_window_upwelling)

    solver = FiniteSolver(
        final_section,
        constraints=solver_constraints)

    return solver(
        duration=start-present,
        steps=steps,
        plot_options=plot_opts)

def solve():
    # This does the computational heavy lifting
    data = dict(
        monterey=monterey_plate(),
        farallon_70=farallon_plate(u(140, "Myr"),u(70,"Myr")),
        farallon_80=farallon_plate(u(145, "Myr"),u(80,"Myr")),
        farallon_60=farallon_plate(u(135, "Myr"),u(60,"Myr")),
        underplating=underplating())

    data = {k:list(v.into("degC")) for k,v in data.items()}

    fn = results_dir("models.json")
    with open(str(fn),"w") as f:
        json.dump(data, f)

