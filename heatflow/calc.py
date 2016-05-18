"""
Solver for geothermal models related to the Crystal Knob xenoliths
"""
from __future__ import division, print_function
from click import echo, secho, style
from functools import partial

from geotherm.models.geometry import Section, stack_sections
from geotherm.solvers import FiniteSolver, AdiabatSolver, steady_state
from geotherm.units import u

from .database import db
from .database.models import StaticProfile
from .model_base import ModelRunner
from .subduction import SubductionCase
from .config import (
    oceanic_mantle,
    continental_crust,
    interface_depth,
    total_depth,
    asthenosphere_temperature,
    solver_constraints,
    present)

class ForearcCase(SubductionCase):
    """
    All of the cases with a forearc geotherm look similar in
    form, with the only differences being the timing of initial
    emplacemnt on the ocean floor and subduction.
    """
    name_base = 'forearc'
    def __init__(self, sub_age, oc_age):
        self.name = "{0}-{1}-{2}".format(self.name_base,sub_age,oc_age)
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
    name_base = 'farallon'
    def __init__(self):
        self.name = self.name_base
        SubductionCase.__init__(self,u(130,"Myr"),u(75,"Myr"))
        # Solve to imaginary model division to make
        # model outputs align with farallon-reheated case
        self.fake_underplating_time = u(24,'Myr')

    def setup(self):
        self.pre_subduction()
        self.stepped_subduction(final_temperature=u(700,"degC"))

    def run(self):
        self.setup()

        # Pause at 24 Ma to record a fake timestep
        self.finite_solve(self.fake_underplating_time)
        __recs = ('before-underplating','underplating-started','after-underplating')
        for i in __recs:
            self.record(i)

        self.solve_to_present()

class UnderplatingMixin(object):
    def do_underplating(self):
        self.record("before-underplating")

        dT = self.underplating_duration

        temp = asthenosphere_temperature

        adiabat = AdiabatSolver(
            self.section,
            start_depth=self.underplating_depth,
            start_temp=temp)
        # Apply adiabat to section
        self.section = adiabat()

        self.record("underplating-started", self.section)

        if dT.into('s') > 0:
            # We're holding the temperature
            # at the boundary for some length of time
            top, bottom = self.section.divide(self.underplating_depth)

            solver = FiniteSolver(top,
                constraints=(u(0,'degC'),temp),
                step_function=self.step_function)

            dTdz = adiabat.gradient[0]
            k = bottom.material_property('conductivity')[0]
            flux = -k*dTdz

            solver.set_constraints(lower=flux)
            res = solver(dT).profile
            self.section.profile[:len(res)] = res
            self.t -= dT

        self.record("underplating-ended")
        # Record a later timestep
        dT =  u(6,'Myr') - dT
        if dT > u(0,'s'):
            self.finite_solve(self.t-dT)
        self.record("after-underplating")

class FarallonReheated(Farallon, UnderplatingMixin):
    """
    Deep (90 km) underplating
    of mantle lithosphere at 1450 (Tmax for GDHsolver) degC
    """
    name_base = 'farallon-reheated'
    def __init__(self, dT):
        Farallon.__init__(self)
        self.name = self.name_base+'-'+str(dT)
        self.underplating_duration = u(dT,'Myr')
        self.underplating_depth = u(80,'km')
        self.underplating_time = u(24,'Myr')

    def run(self):
        self.setup()
        self.finite_solve(self.underplating_time)
        self.do_underplating()
        self.solve_to_present()

class Underplated(ModelRunner, UnderplatingMixin):
    name_base = 'underplated'
    def __init__(self, dT):
        ModelRunner.__init__(self)
        self.name = self.name_base+'-'+str(dT)
        self.underplating_duration = u(dT,'Myr')
        self.underplating_depth = u(30,'km')
        self.underplating_time = u(24,'Myr')
        self.start_time = self.underplating_time

    def run(self):

        plot_opts = dict(
            range=(0,1500))

        crust = continental_crust.to_layer(interface_depth)
        solver = FiniteSolver(crust,
            constraints=(u(0,"degC"),u(600,"degC")))
        # Assume arbitrarily that interface is at 600 degC

        crust_section = solver.steady_state()

        mantle = oceanic_mantle.to_layer(total_depth-interface_depth)
        mantle = Section([mantle])

        # Set starting state
        section = stack_sections(crust_section, mantle)
        adiabat = AdiabatSolver(
            section,
            start_depth=self.underplating_depth,
            start_temp=asthenosphere_temperature)

        self.t = self.start_time
        self.section = adiabat()
        self.record("initial")
        self.do_underplating()
        self.solve_to_present()

class SteadyState(ModelRunner):
    """
    Steady-state case for 30 km of crust
    atop 270 km of oceanic mantle
    """
    name = 'steady-state'

    def setup_recorder(self):
        self.session = db.session()
        n_deleted = self.session.query(StaticProfile).delete()
        if n_deleted > 0:
            secho("Deleting data from previous run", fg='red')
        self.session.commit()

    def record(self, section, flux):
        T, dz = self.section_data(section)
        v = StaticProfile(
            heat_flow=flux,
            temperature=T,
            dz=dz)
        self.session.add(v)

    def run(self):
        section = Section([
            continental_crust.to_layer(interface_depth),
            oceanic_mantle.to_layer(total_depth-interface_depth)])

        for flux in (90,95,100):
            q = u(flux,'mW/m^2')
            s = steady_state(section,q)
            self.record(s,flux)
            echo("Saving section for "
                 +style(str(q), fg='green')
                 +" surface heat flux")


