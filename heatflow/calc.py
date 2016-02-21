"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
from click import echo
from functools import partial

from geotherm.models.geometry import Section, stack_sections
from geotherm.solvers import GDHSolver, FiniteSolver, RoydenSolver, AdiabatSolver
from geotherm.units import u

from .config import (
    oceanic_mantle,
    continental_crust,
    interface_depth,
    total_depth,
    solver_constraints,
    present)

from .model_base import ModelRunner
from .subduction import SubductionCase

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
        self.pre_subduction()
        self.stepped_subduction()
        self.solve_to_present()

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
        self.pre_subduction()
        self.stepped_subduction(final_temperature=u(700,"degC"))

    def run(self):
        self.setup()
        self.solve_to_present()

class FarallonReheated(Farallon):
    """
    Deep (90 km) underplating
    of mantle lithosphere at 1450 (Tmax for GDHsolver) degC
    """
    name = 'farallon-reheated'

    def run(self):

        underplating_depth = u(90,'km')
        underplating_time = u(20,'Myr')

        self.setup()
        self.finite_solve(underplating_time)
        self.record("before-underplating")

        dT = u(2,'Myr')

        temp = GDHSolver.defaults["T_max"]

        if dT is not None:
            # We're holding the temperature
            # at the boundary for some length of time
            top_section = self.section.get_slice(u(0,'km'),underplating_depth)
            solver = FiniteSolver(top_section,
                constraints=(u(0,'degC'),temp),
                step_function=self.step_function)
            res = solver(dT).profile
            self.section.profile[:len(res)] = res
            self.t -= dT

        apply_adiabat = AdiabatSolver(
            start_depth=underplating_depth,
            start_temp=temp)

        self.section = apply_adiabat(self.section)
        self.record("after-underplating")
        self.solve_to_present()

class Underplated(ModelRunner):
    name = 'underplated'
    def run(self):

        plot_opts = dict(
            range=(0,1500))

        start = u(20,"Myr")

        crust = continental_crust.to_layer(interface_depth)
        solver = FiniteSolver(crust,
            constraints=(u(0,"degC"),u(600,"degC")))
        # Assume arbitrarily that interface is at 600 degC

        crust_section = solver.steady_state()

        mantle = oceanic_mantle.to_layer(total_depth-interface_depth)
        mantle = Section([mantle])

        # Set starting state
        section = stack_sections(crust_section, mantle)

        apply_adiabat = AdiabatSolver(
            start_depth=interface_depth,
            start_temp=u(1450,"degC"))

        self.t = start
        self.section = apply_adiabat(section)
        self.record("initial")
        self.solve_to_present()

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
        self.set_state(present, solver.steady_state())
        self.record("final")
