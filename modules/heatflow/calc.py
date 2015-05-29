"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
import os, json
from click import echo

from functools import partial
import matplotlib
matplotlib.use("TkAgg")

from geotherm.models.geometry import Section, Layer
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
    u(1400,"degC"))
    #u(48,"mW/m**2"))
    # Globally averaged mantle heat flux from Pollack, et al., 1977

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

    record = partial(save_info, name)

    oceanic = Section([
        oceanic_crust.to_layer(u(7,"km")),
        oceanic_mantle.to_layer(u(263,"km"))])

    apply_adiabat = AdiabatSolver()

    initial_section = apply_adiabat(oceanic)

    record("initial", initial_section, t=start_time)

    t = start_time - subduction_time
    underplated_oceanic = finite_solve(initial_section, t)

    record("before-subduction", underplated_oceanic, t=subduction_time)
    elapsed_time, section = stepped_subduction(
            underplated_oceanic,
            distance=u(100,"km"),
            velocity=u(100,"mm/yr"),
            depth=u(30,"km"))

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

    interface = u(30,"km")

    section = Section([
        continental_crust.to_layer(interface),
        oceanic_mantle.to_layer(u(300,"km")-interface)
        ],
        uniform_temperature=u(400,"degC"))

    apply_adiabat = AdiabatSolver(
        start_depth=interface,
        start_temp=u(1300,"degC"))

    section = apply_adiabat(section)
    record("initial", section, t=start)

    final_section = finite_solve(section,start-present)

    record("final", final_section, t=present)

