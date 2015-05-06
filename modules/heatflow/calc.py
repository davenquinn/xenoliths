"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
import os, json
from click import echo

from functools import partial
import matplotlib
matplotlib.use("TkAgg")

from geotherm.units import u
from geotherm.models.geometry import Section, Layer, stack_sections
from geotherm.solvers import HalfSpaceSolver, FiniteSolver, RoydenSolver, AdiabatSolver
from geotherm.materials import oceanic_mantle, continental_crust, oceanic_crust
from geotherm.plot import Plotter

from .forearc import forearc_section
from .util import mkdirs
from . import results_dir

present = u(1.65,"Myr") # K-Ar age for Crystal Knob xenoliths

solver_constraints = (
    u(20,"degC"), # Surface temperature
    u(1500,"degC"))
    #u(48,"mW/m**2"))
    # Globally averaged mantle heat flux from Pollack, et al., 1977

T_lithosphere = u(1300,"degC")

plotter = Plotter(range=(0,1400))

FiniteSolver.set_defaults(
    type="implicit",
    time_step=u(1,"Myr"),
    constraints=solver_constraints,
    plotter=plotter)

def finite_solve(section, duration):
    constraints = (u(20,"degC"), section.profile[-1])
    echo("Initializing finite solver with constraints "
            "{0} and {1}".format(*constraints))

    solver = FiniteSolver(section, constraints=constraints)
    return solver(duration)

def save_info(name, step, section):
    out = dict(
        T=list(section.profile.into("degC")),
        z=list(section.cell_centers.into("m")))

    fn = step+".json"
    path = results_dir(name,fn)

    mkdirs(os.path.dirname(path))
    print("Saving profile to",path)
    with open(path,"w") as f:
        json.dump(out,f)

def subduction_case(name, start_time, subduction_time):
    """Both the Monterey and Farallon-Plate scenarios involve the same
    basic steps, just with different timing.
    """
    print(name)

    record = partial(save_info, name)

    oceanic = Section([
        oceanic_crust.to_layer(u(7,"km")),
        oceanic_mantle.to_layer(u(263,"km"))])

    apply_adiabat = AdiabatSolver()

    initial_section = apply_adiabat(oceanic)

    record("initial", initial_section)

    t = start_time - subduction_time
    underplated_oceanic = finite_solve(initial_section, t)

    record("before-subduction", underplated_oceanic)

    # Find the base of the lithosphere
    d = underplated_oceanic.depth(T_lithosphere)
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

    final_section = finite_solve(section, subduction_time-present)

    record("final",final_section)

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
    record("initial", section)

    final_section = finite_solve(section,start-present)

    record("final", final_section)

def solve():
    # This does the computational heavy lifting

    scenarios = [
        (80,60),(70,50),(60,40),(50,30),(40,20),(30,10),(28,2)]

    for sub_age,oc_age in scenarios:
        subduction_case("forearc-{0}-{1}".format(sub_age,oc_age),
            u(sub_age+oc_age,"Myr"), u(sub_age,"Myr"))

    #subduction_case("monterey-plate",u(28,"Myr"),u(26,"Myr"))
    #subduction_case("farallon-intermediate",u(140, "Myr"),u(70,"Myr"))
    #subduction_case("farallon-old",u(145, "Myr"),u(80,"Myr"))
    #subduction_case("farallon-young",u(135, "Myr"),u(60,"Myr"))
    underplating()

def solve_gradient():
    pass
