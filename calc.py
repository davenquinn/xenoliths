"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
import os, json
from click import echo

from functools import partial

from geotherm.units import u
from geotherm.models.geometry import Section, Layer, stack_sections
from geotherm.solvers import HalfSpaceSolver, FiniteSolver, RoydenSolver
from geotherm.materials import oceanic_mantle, continental_crust

from .scenario import ModelScenario
from .forearc import forearc_section
from .util import mkdirs
from . import results_dir

present = u(1.65,"Myr") # K-Ar age for Crystal Knob xenoliths

solver_constraints = (
    u(20,"degC"), # Surface temperature
    u(1500,"degC"))
    #u(48,"mW/m**2"))
    # Globally averaged mantle heat flux from Pollack, et al., 1977

steps = 50

T_lithosphere = u(1300,"degC")

def save_info(name, step, section):
    out = dict(
        T=list(section.profile.into("degC")),
        z=list(section.cell_centers.into("m")))

    fn = step+".json"
    path = results_dir(name,fn)

    mkdirs(os.path.dirname(path))

    with open(path,"w") as f:
        json.dump(out,f)

def subduction_case(name, start_time, subduction_time):
    """Both the Monterey and Farallon-Plate scenarios involve the same
    basic steps, just with different timing.
    """
    print(name)

    record = partial(save_info, name)

    oceanic = Section([oceanic_mantle.to_layer(u(250,"km"))])

    half_space = HalfSpaceSolver(oceanic)
    initial = half_space(u(0,"yr"))

    record("initial", initial)

    t = start_time-subduction_time
    underplated_oceanic = half_space(t)

    record("before-subduction", underplated_oceanic)

    # Find the base of the lithosphere
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

    section = stack_sections(
        forearc,
        underplated_oceanic)

    record("after-subduction", section)

    solver = FiniteSolver(
        section,
        constraints=solver_constraints)

    final_section = solver(
        subduction_time-present,
        steps=steps)

    record("final",final_section)

farallon_plate = partial(
    subduction_case,
    "farallon_plate")

def underplating():
    name = "underplating"
    record = partial(save_info, name)

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

    section = stack_sections(
        forearc,
        slab_window_upwelling)

    record("initial", section)

    solver = FiniteSolver(
        section,
        constraints=solver_constraints)

    final = solver(
        duration=start-present,
        steps=steps,
        plot_options=plot_opts)

    record("final", section)

def solve():
    # This does the computational heavy lifting
    subduction_case("monterey-plate",u(28,"Myr"),u(26,"Myr"))
    subduction_case("farallon-intermediate",u(140, "Myr"),u(70,"Myr"))
    subduction_case("farallon-old",u(145, "Myr"),u(80,"Myr"))
    subduction_case("farallon-young",u(135, "Myr"),u(60,"Myr"))
    underplating()

