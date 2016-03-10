# -*- coding: utf-8 -*-

from __future__ import division
import numpy as N
from click import echo
from geotherm.units import u
from geotherm.models.geometry import Section, stack_sections
from .forearc import forearc_section, forearc_solver, optimized_forearc
from .model_base import ModelRunner
from .config import (
        oceanic_mantle,
        total_depth,
        solver_constraints,
        asthenosphere_temperature,
        forearc_base_temperature,
        interface_depth,
        convergence_velocity,
        underplating_distance)
from geotherm.solvers import GDHSolver, FiniteSolver, RoydenSolver, AdiabatSolver
from geotherm.materials import continental_crust

def lithosphere_depth(underplated_section):
    # Find the base of the lithosphere
    d = underplated_section.depth(forearc_base_temperature)
    echo("Depth of the base of the "
        "lithosphere at the time of "
        "subduction:{0:.2f}".format(d))
    return d

class SubductionCase(ModelRunner):
    """
    Base model runner for all of the cases which involve
    cooling of oceanic crust followed by subduction.
    """
    def __init__(self, start_time, subduction_time):
        ModelRunner.__init__(self)
        self.start_time = start_time
        self.subduction_time = subduction_time
        # Depths in the main section are less than present depths
        self.depth_offset = interface_depth

    def pre_subduction(self):
        """
        Get an oceanic geotherm at emplacement and just before
        subduction begins.
        """
        self.log("Start age", self.start_time)
        self.log("Subduction", self.subduction_time)

        oceanic = Section([
            oceanic_mantle.to_layer(total_depth-interface_depth)])

        ocean_model = GDHSolver(oceanic, T_max=solver_constraints[1])
        t = u(0,"s")
        self.set_state(self.start_time,ocean_model(t))
        self.record("initial")

        dt = self.t - self.subduction_time
        self.set_state(self.subduction_time, ocean_model(dt))
        self.record("before-subduction")

    def instant_subduction(self, **kwargs):
        d = asthenosphere_depth(self.section)
        forearc = forearc_section(
                distance = underplating_distance,
                Tm = asthenosphere_temperature.into("degC"),
                l = d.into("m"))
        self.log("Temperature at subduction interface "
             "at the time of underplating", forearc.profile[-1])
        self.section = stack_sections(forearc, self.section)

    def stepped_subduction(self, **kwargs):
        """
        Method to subduct crust under a forearc
        with a geotherm modeled over a period of
        time, and capture a snapshot of underplating.

        The `velocity` option defines a subduction velocity
        that is used to move the subducting slab down the
        channel.

        If the `final_temperature` option is not set,
        the procedure will infer the final temperature
        of the subducted slab from a steady-state subduction
        geometery, using the method of Royden (1992).

        If the `final_temperature` option is set,
        the procedure will target that temperature
        at the final conditions of the interface.
        In this case, the Royden model parameters
        for this temperature will be found via optimization.
        """

        final_distance = kwargs.pop("final_distance", underplating_distance)
        velocity = kwargs.pop("velocity", convergence_velocity)
        final_depth = kwargs.pop("final_depth", interface_depth)

        final_temperature = kwargs.pop("final_temperature", None)

        # Thickness of foreland lithosphere
        # at the time of subduction
        # Presumably, foreland in this case refers
        # to the lower plate of the thrust advancing
        # into the subduction zone
        # The Royden model assumes that the foreland
        # is in thermal equilibrium, and the lithospheric
        # depth is being maintained, which is likely a
        # reasonable approximation for the timescales involved.
        self.log("Subduction velocity",velocity)

        dip = N.arctan(final_depth/final_distance).to("degrees")
        self.log("Dip of subduction zone",dip)

        # distance along subduction channel
        sub_distance = N.sqrt(final_distance**2+final_depth**2)
        duration = (sub_distance/velocity).to("Myr")
        self.log("Duration of subduction",duration)

        echo("Beginning to subduct slab")

        kwargs.update(
            l=lithosphere_depth(self.section).into("m"),
            v=velocity.into("m/s"))

        self.log("Lithosphere depth", kwargs['l'])

        if final_temperature is None:
            royden = forearc_solver(**kwargs)
        else:
            # Optimize on rate of accretion
            royden = optimized_forearc(
                final_temperature,
                final_distance,
                final_depth,
                **kwargs)
            self.log("Modeled friction along fault",royden.args['qfric'])

        def on_step(solver, **kwargs):
            """
            Function to change finite solver
            boundary conditions at each step
            """
            self.step_function(solver, **kwargs)

            step = kwargs.pop("step")
            steps = kwargs.pop("steps")

            # How complete we will be at the
            # end of this step
            completion = (step+1)/steps

            sz_depth = final_depth*completion
            # Decrease depth offset
            self.depth_offset = final_depth-sz_depth

            # Set temperature at the subduction
            # interface
            T = royden(
                (final_distance*completion).into("m"),
                sz_depth.into("m"), # Depth of interest
                sz_depth.into("m")) # Depth of subduction interface

            solver.set_constraints(upper=u(T,"degC"))

        # Set up finite solving for underplated slab
        kwargs['step_function'] = on_step
        i = self.section.profile[-1]
        solver = FiniteSolver(self.section,
            constraints=(u(0,'degC'),i))
        underplated = solver.final_section(
            duration=duration,
            **kwargs)

        # Construct the forearc geotherm
        forearc = Section(continental_crust
                .to_layer(final_depth))

        temperatures = royden(
            final_distance.into("m"),
            forearc.cell_centers.into("m"),
            final_depth.into("m"))

        forearc.profile = u(temperatures, "degC")

        self.log("Temperature at subduction interface "
             "at the time of underplating", forearc.profile[-1])
        self.log("Subduction took",duration.to("Myr"))

        self.section = stack_sections(forearc, underplated)
        self.t -= duration
        self.depth_offset = u(0,'km')
        self.record("after-subduction")
