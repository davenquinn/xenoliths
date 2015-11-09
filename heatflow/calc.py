"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
import os, json
from click import echo

from functools import partial
import matplotlib
matplotlib.use("TkAgg")

from geotherm.models.geometry import Section, stack_sections
from geotherm.solvers import HalfSpaceSolver, FiniteSolver, RoydenSolver, AdiabatSolver
from geotherm.materials import oceanic_mantle, continental_crust, oceanic_crust
from geotherm.plot import Plotter
from geotherm.units import u

from .subduction import instant_subduction, stepped_subduction
from .util import mkdirs
from . import results_dir

present = u(1.65,"Myr") # K-Ar age for Crystal Knob xenoliths

solver_constraints = (
    u(0,"degC"), # Surface temperature
    u(1500,"degC"))
    #u(48,"mW/m**2"))
    # Globally averaged mantle heat flux from Pollack, et al., 1977

interface_depth = u(30,'km')
total_depth = u(500,'km')

plotter = Plotter(range=(0,1400))

FiniteSolver.set_defaults(
    type="implicit",
    time_step=u(1,"Myr"),
    constraints=solver_constraints,
    plotter=plotter)

def finite_solve(section, duration):
    constraints = (u(0,"degC"), section.profile[-1])
    echo("Initializing finite solver with constraints "
            "{0} and {1}".format(*constraints))

    solver = FiniteSolver(section, constraints=constraints)
    return solver(duration)

def save_info(name, step, section, **kwargs):
    if "t" in kwargs:
        kwargs["t"] = kwargs["t"].into("Myr")

    out = dict(
        T=list(section.profile.into("degC")),
        z=list(section.cell_centers.into("m")),
        **kwargs)

    fn = step+".json"
    path = results_dir(name,fn)

    mkdirs(os.path.dirname(path))
    print("Saving profile to",path)
    with open(path,"w") as f:
        json.dump(out,f)

def forearc_case(name, start_time, subduction_time):
    """
    All of the cases with a forearc geotherm look similar in
    form, with the only differences being the timing of initial
    emplacemnt on the ocean floor and subduction.
    """
    print(name)

    interface = u(30,'km')

    record = partial(save_info, name)

    oceanic = Section([
        oceanic_mantle.to_layer(total_depth-interface_depth)])

    ocean_model = HalfSpaceSolver(oceanic)

    record("initial", ocean_model(u(0,"s")), t=start_time)

    t = start_time - subduction_time
    underplated_oceanic = ocean_model(t)

    record("before-subduction", underplated_oceanic, t=subduction_time)
    elapsed_time, section = stepped_subduction(
            underplated_oceanic,
            final_distance=u(100,"km"),
            velocity=u(100,"mm/yr"),
            final_depth=u(30,"km"))

    echo("Subduction took {}".format(elapsed_time.to("Myr")))

    t = subduction_time-elapsed_time
    record("after-subduction", section, t=t)
    final_section = finite_solve(section,
            t-present)

    record("final",final_section,t=present)

def farallon_case():
    """
    Similar to the forearc-geotherm case, but with the
    temperature under the slab pinned to 700 degC at 10kb,
    a constraint garnered from the Rand Schist
    """
    record = partial(save_info, "farallon")

    start_time = u(140,"Myr")
    subduction_time = u(80,"Myr")

    oceanic = Section([
        oceanic_mantle.to_layer(u(270,"km"))])

    ocean_model = HalfSpaceSolver(oceanic)

    record("initial", ocean_model(u(0,"s")), t=start_time)

    t = start_time - subduction_time
    underplated_oceanic = ocean_model(t)

    record("before-subduction", underplated_oceanic, t=subduction_time)
    elapsed_time, section = stepped_subduction(
            underplated_oceanic,
            final_distance=u(100,"km"),
            velocity=u(100,"mm/yr"),
            final_temperature=u(700,"degC"),
            final_depth=interface_depth)

    echo("Subduction took {}".format(elapsed_time.to("Myr")))

    t = subduction_time-elapsed_time
    record("after-subduction", section, t=t)
    final_section = finite_solve(section,
            t-present)

    record("final",final_section,t=present)


def underplating():
    name = "underplating"
    record = partial(save_info, name)

    plot_opts = dict(
        range=(0,1500),
        title=name)

    start = u(20,"Myr")

    crust = continental_crust.to_layer(interface_depth)
    solver = FiniteSolver(crust,constraints=(
        u(0,"degC"),u(600,"degC")))
    # Assume arbitrarily that interface is at 600 degC

    crust_section = Section([crust],
        profile=solver.steady_state())

    mantle = oceanic_mantle.to_layer(total_depth-interface_depth)
    mantle = Section(mantle)

    section = stack_sections(crust_section, mantle)

    apply_adiabat = AdiabatSolver(
        start_depth=interface,
        start_temp=u(1300,"degC"))

    section = apply_adiabat(section)
    record("initial", section, t=start)

    final_section = finite_solve(section,start-present)

    record("final", final_section, t=present)

def steady_state():
    """
    Steady-state case for 30 km of crust
    atop 270 km of oceanic mantle
    """
    record = partial(save_info, "steady-state")

    section = Section([
        crust.to_layer(u(30,"km")),
        oceanic_mantle.to_layer(total_depth-interface_depth)])

    solver = FiniteSolver(section)

    record("steady-state",solver.steady_state())
