# -*- coding: utf-8 -*-

from __future__ import division
import numpy as N
from click import echo
from geotherm.units import u
from geotherm.models.geometry import Section, stack_sections
from .forearc import forearc_section, forearc_solver, optimized_forearc
from .config import (
        asthenosphere_temperature,
        interface_depth,
        convergence_velocity,
        underplating_distance)
from geotherm.solvers import FiniteSolver
from geotherm.materials import continental_crust

def lithosphere_depth(underplated_section):
    # Find the base of the lithosphere
    d = underplated_section.depth(asthenosphere_temperature)
    echo("Depth of the base of the "
        "lithosphere at the time of "
        "subduction:{0:.2f}".format(d))
    return d

def instant_subduction(underplated_section, **kwargs):
    d = asthenosphere_depth(underplated_section)
    forearc = forearc_section(
            distance = underplating_distance,
            Tm = asthenosphere_temperature.into("degC"),
            l = d.into("m"))
    echo("Temperature at subduction interface "
         "at the time of underplating: {0}"\
          .format(forearc.profile[-1]))

    return stack_sections(
        forearc, underplated_section)

def stepped_subduction(underplated_section, **kwargs):
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
    step_function = kwargs.pop("step_function", None)

    # Thickness of foreland lithosphere
    # at the time of subduction
    # Presumably, foreland in this case refers
    # to the lower plate of the thrust advancing
    # into the subduction zone
    # The Royden model assumes that the foreland
    # is in thermal equilibrium, and the lithospheric
    # depth is being maintained, which is likely a
    # reasonable approximation for the timescales involved.
    echo("Subduction velocity: {}".format(velocity))

    dip = N.arctan(final_depth/final_distance).to("degrees")
    echo("Dip of subduction zone: {}".format(dip))

    # distance along subduction channel
    sub_distance = N.sqrt(final_distance**2+final_depth**2)

    duration = (sub_distance/velocity).to("Myr")

    echo("Duration of subduction: {}".format(duration))

    echo("Beginning to subduct slab")

    kwargs.update(
        l=lithosphere_depth(underplated_section).into("m"),
        v=velocity.into("m/s"))

    if final_temperature is None:
        royden = forearc_solver(**kwargs)
    else:
        # Optimize on rate of accretion
        royden = optimized_forearc(
            final_temperature,
            final_distance,
            final_depth,
            **kwargs)
        echo("Modeled friction along fault: {0}"
                .format(royden.args['qfric']))

    def on_step(solver, **kwargs):
        """ Function to change finite solver
            boundary conditions at each step
        """
        if step_function is not None:
            step_function(solver, **kwargs)

        step = kwargs.pop("step")
        steps = kwargs.pop("steps")

        # How complete we will be at the
        # end of this step
        completion = (step+1)/steps

        sz_depth = final_depth*completion

        # Set temperature at the subduction
        # interface
        T = royden(
            (final_distance*completion).into("m"),
            sz_depth.into("m"), # Depth of interest
            sz_depth.into("m")) # Depth of subduction interface

        solver.set_constraints(upper=u(T,"degC"))

        # Estimate heat flux at base of foreac
        t = royden(
            (final_distance*completion).into("m"),
            sz_depth.into("m")-1, # Depth of interest
            sz_depth.into("m")) # Depth of subduction interface

        dT = u(T-t,'K/m')
        k = u(royden.args['Ku'],'W/(m K)')
        heat_flux = k*dT
        #solver.set_constraints(upper=heat_flux)


    # Set up finite solving for underplated slab
    solver = FiniteSolver(underplated_section,
        constraints=(u(0,"degC"), underplated_section.profile[-1]))

    underplated_section = solver.final_section(
        duration=duration,
        step_function=on_step,
        **kwargs)

    # Construct the forearc geotherm
    forearc = Section(continental_crust
            .to_layer(final_depth))

    temperatures = royden(
        final_distance.into("m"),
        forearc.cell_centers.into("m"),
        final_depth.into("m"))

    forearc.profile = u(temperatures, "degC")

    echo("Temperature at subduction interface "
         "at the time of underplating: {0} {1}"\
          .format(
              forearc.profile[-1],
              underplated_section.profile[0]))

    s = stack_sections(forearc, underplated_section)

    return duration, s
