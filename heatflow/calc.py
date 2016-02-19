"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
import os, json
from click import echo

from functools import partial, wraps
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
    if kwargs.pop('verbose',False):
        print("Saving profile to",path)
    with open(path,"w") as f:
        json.dump(out,f)

def instrumented(name=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            if name is None:
                # We get name as first argument
                # passed to wrapped function
                args = list(args)
                name = args.pop(0)
                print(args)
            recorder = partial(save_info,name)
            return f(recorder,*args,**kwargs)
        return wrapper
    return decorator

def pre_subduction(record, start_time, subduction_time):
    """
    Get an oceanic geotherm at emplacement and just before
    subduction begins.
    """
    echo("Start age:  {0}".format(start_time))
    echo("Subduction: {0}".format(subduction_time))

    oceanic = Section([
        oceanic_mantle.to_layer(total_depth-interface_depth)])

    ocean_model = GDHSolver(oceanic, T_max=solver_constraints[1])

    record("initial", ocean_model(u(0,"s")), t=start_time)

    t = start_time - subduction_time
    underplated_oceanic = ocean_model(t)

    record("before-subduction", underplated_oceanic, t=subduction_time)

    return underplated_oceanic

@instrumented()
def forearc_case(record, start_time, subduction_time):
    """
    All of the cases with a forearc geotherm look similar in
    form, with the only differences being the timing of initial
    emplacemnt on the ocean floor and subduction.
    """
    underplated_oceanic = pre_subduction(record, start_time, subduction_time)

    elapsed_time, section = stepped_subduction(underplated_oceanic)

    echo("Subduction took {}".format(elapsed_time.to("Myr")))

    t = subduction_time-elapsed_time
    record("after-subduction", section, t=t)
    final_section = finite_solve(section,t-present)

    record("final",final_section,t=present)

def farallon_setup(record):
    """
    Shared setup for Farallon and Farallon-reheated cases
    """
    start_time = u(140,"Myr")
    subduction_time = u(80,"Myr")

    underplated_oceanic = pre_subduction(
        record,
        start_time,
        subduction_time)

    elapsed_time, section = stepped_subduction(
            underplated_oceanic,
            final_temperature=u(700,"degC"))

    echo("Subduction took {}".format(elapsed_time.to("Myr")))

    t = subduction_time-elapsed_time
    record("after-subduction", section, t=t)
    return section, t

@instrumented('farallon')
def farallon_case(record):
    """
    Similar to the forearc-geotherm case, but with the
    temperature under the slab pinned to 700 degC at 10kb,
    a constraint garnered from the Rand Schist
    """
    record = partial(save_info, 'farallon')
    section, t = farallon_setup(record)
    final_section = finite_solve(section,
            t-present)
    record("final",final_section,t=present)

@instrumented('farallon-reheated')
def farallon_reheated(record, dT=None):
    """
    Deep (90 km) underplating
    of mantle lithosphere at 1450 (Tmax for GDHsolver) degC
    """
    underplating_depth = u(90,'km')
    underplating_T = u(20,'Myr')

    section, t = farallon_setup(record)
    section = finite_solve(section, t-underplating_T)

    record("before-underplating", section, t=underplating_T)

    dT = u(2,'Myr')

    temp = GDHSolver.defaults["T_max"]

    if dT is not None:
        # We're holding the temperature
        # at the boundary for some length of time
        top_section = section.get_slice(u(0,'km'),underplating_depth)
        solver = FiniteSolver(top_section,
            constraints=(u(0,'degC'),temp))
        res = solver(dT).profile
        section.profile[:len(res)] = res
        underplating_T -= dT

    apply_adiabat = AdiabatSolver(
        start_depth=underplating_depth,
        start_temp=temp)

    section = apply_adiabat(section)

    record("after-underplating", section, t=underplating_T)

    final_section = finite_solve(section,underplating_T-present)

    record("final", final_section, t=present)

@instrumented('underplated')
def underplating(record):

    plot_opts = dict(
        range=(0,1500))

    start = u(20,"Myr")

    crust = continental_crust.to_layer(interface_depth)
    solver = FiniteSolver(crust,constraints=(
        u(0,"degC"),u(600,"degC")))
    # Assume arbitrarily that interface is at 600 degC

    crust_section = solver.steady_state()

    mantle = oceanic_mantle.to_layer(total_depth-interface_depth)
    mantle = Section([mantle])

    section = stack_sections(crust_section, mantle)

    apply_adiabat = AdiabatSolver(
        start_depth=interface_depth,
        start_temp=u(1450,"degC"))

    section = apply_adiabat(section)
    record("initial", section, t=start)

    final_section = finite_solve(section,start-present)

    record("final", final_section, t=present)

@instrumented('steady-state')
def steady_state(record):
    """
    Steady-state case for 30 km of crust
    atop 270 km of oceanic mantle
    """
    section = Section([
        continental_crust.to_layer(interface_depth),
        oceanic_mantle.to_layer(total_depth-interface_depth)])

    solver = FiniteSolver(section)

    record("final",solver.steady_state())
