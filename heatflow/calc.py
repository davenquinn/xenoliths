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
from geotherm.solvers import GDHSolver, HalfSpaceSolver, FiniteSolver, RoydenSolver, AdiabatSolver
from geotherm.plot import Plotter
from geotherm.units import u

from .config import (
    oceanic_mantle,
    continental_crust,
    interface_depth,
    total_depth,
    solver_constraints,
    present)

from .subduction import instant_subduction, stepped_subduction
from .util import mkdirs
from . import results_dir

plotter = Plotter(range=(0,1400))

FiniteSolver.set_defaults(
    type="implicit",
    time_step=u(0.5,"Myr"),
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

def pre_subduction(name, start_time, subduction_time):
    """
    Get an oceanic geotherm at emplacement and just before
    subduction begins.
    """
    echo("Start age:  {0}".format(start_time))
    echo("Subduction: {0}".format(subduction_time))

    record = partial(save_info, name)

    oceanic = Section([
        oceanic_mantle.to_layer(total_depth-interface_depth)])

    ocean_model = GDHSolver(oceanic, T_max=solver_constraints[1])

    record("initial", ocean_model(u(0,"s")), t=start_time)

    t = start_time - subduction_time
    underplated_oceanic = ocean_model(t)

    record("before-subduction", underplated_oceanic, t=subduction_time)

    return underplated_oceanic

def forearc_case(name, start_time, subduction_time):
    """
    All of the cases with a forearc geotherm look similar in
    form, with the only differences being the timing of initial
    emplacemnt on the ocean floor and subduction.
    """
    record = partial(save_info, name)

    underplated_oceanic = pre_subduction(name, start_time, subduction_time)

    elapsed_time, section = stepped_subduction(underplated_oceanic)

    echo("Subduction took {}".format(elapsed_time.to("Myr")))

    t = subduction_time-elapsed_time
    record("after-subduction", section, t=t)
    final_section = finite_solve(section,t-present)

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

    underplated_oceanic = pre_subduction(
        "farallon",
        start_time,
        subduction_time)

    elapsed_time, section = stepped_subduction(
            underplated_oceanic,
            final_temperature=u(700,"degC"))

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
        crust.to_layer(interface_depth),
        oceanic_mantle.to_layer(total_depth-interface_depth)])

    solver = FiniteSolver(section)

    record("steady-state",solver.steady_state())
