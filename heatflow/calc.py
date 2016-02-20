"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
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

from .model_base import ModelRunner
from .subduction import instant_subduction, stepped_subduction

plotter = Plotter(range=(0,1500))

FiniteSolver.set_defaults(
    type="implicit",
    time_step=u(0.5,"Myr"),
    constraints=solver_constraints,
    plotter=plotter)

def step_function(self, model, time, step, n_steps):
    """
    Step function for finite element solver that records model tracers
    """
    import IPython; IPython.embed()

def finite_solve(section, duration, **kwargs):
    constraints = (u(0,"degC"), section.profile[-1])
    echo("Initializing finite solver with constraints "
            "{0} and {1}".format(*constraints))

    solver = FiniteSolver(section, constraints=constraints, **kwargs)
    return solver(duration)

class SubductionCase(ModelRunner):
    """
    Base model runner for all of the cases which involve
    cooling of oceanic crust followed by subduction.
    """
    def __init__(self, start_time, subduction_time):
        self.start_time = start_time
        self.subduction_time = subduction_time

    def pre_subduction(self):
        """
        Get an oceanic geotherm at emplacement and just before
        subduction begins.
        """
        echo("Start age:  {0}".format(self.start_time))
        echo("Subduction: {0}".format(self.subduction_time))

        oceanic = Section([
            oceanic_mantle.to_layer(total_depth-interface_depth)])

        ocean_model = GDHSolver(oceanic, T_max=solver_constraints[1])

        self.record("initial", ocean_model(u(0,"s")), t=self.start_time)

        t = self.start_time - self.subduction_time
        underplated_oceanic = ocean_model(t)

        self.record("before-subduction", underplated_oceanic, t=self.subduction_time)

        return underplated_oceanic

class ForearcCase(SubductionCase):
    """
    All of the cases with a forearc geotherm look similar in
    form, with the only differences being the timing of initial
    emplacemnt on the ocean floor and subduction.
    """
    def __init__(self, sub_age, oc_age):
        self.name = "forearc-{0}-{1}".format(sub_age,oc_age)
        args = (u(sub_age+oc_age,"Myr"), u(sub_age,"Myr"))
        SubductionCase.__init__(self, *args)

    def run(self):
        underplated_oceanic = self.pre_subduction()

        elapsed_time, section = stepped_subduction(underplated_oceanic)

        echo("Subduction took {}".format(elapsed_time.to("Myr")))

        t = subduction_time-elapsed_time
        self.record("after-subduction", section, t=t)
        final_section = finite_solve(section,t-present)

        self.record("final",final_section,t=present)

class Farallon(SubductionCase):
    """
    Similar to the forearc-geotherm case, but with the
    temperature under the slab pinned to 700 degC at 10kb,
    a constraint garnered from the Rand Schist
    """
    name = 'farallon'
    def __init__(self):
        self.start_time = u(140,"Myr")
        self.subduction_time = u(80,"Myr")

    def setup(self):
        underplated_oceanic = self.pre_subduction()

        elapsed_time, section = stepped_subduction(
                underplated_oceanic,
                final_temperature=u(700,"degC"))

        echo("Subduction took {}".format(elapsed_time.to("Myr")))

        t = self.subduction_time-elapsed_time
        self.record("after-subduction", section, t=t)
        return section, t

    def run(self):
        section, t = self.setup()
        final_section = finite_solve(section,
                t-present)
        self.record("final",final_section,t=present)

class FarallonReheated(Farallon):
    """
    Deep (90 km) underplating
    of mantle lithosphere at 1450 (Tmax for GDHsolver) degC
    """
    name = 'farallon-reheated'

    def run(self):

        underplating_depth = u(90,'km')
        underplating_T = u(20,'Myr')

        section, t = self.setup()
        section = finite_solve(section, t-underplating_T)

        self.record("before-underplating", section, t=underplating_T)

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

        self.record("after-underplating", section, t=underplating_T)

        final_section = finite_solve(section,underplating_T-present)

        self.record("final", final_section, t=present)

class Underplated(ModelRunner):
    name = 'underplated'
    def run(self):

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
        self.record("initial", section, t=start)

        final_section = finite_solve(section,start-present)

        self.record("final", final_section, t=present)

class SteadyState(ModelRunner):
    """
    Steady-state case for 30 km of crust
    atop 270 km of oceanic mantle
    """
    name = 'steady-state'
    def run(self):
        section = Section([
            continental_crust.to_layer(interface_depth),
            oceanic_mantle.to_layer(total_depth-interface_depth)])
        solver = FiniteSolver(section)
        self.record("final",solver.steady_state())
