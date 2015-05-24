# -*- coding: utf-8 -*-

from __future__ import division
import numpy as N
from click import echo
from geotherm.units import u
from geotherm.models.geometry import stack_sections
from .forearc import forearc_section, forearc_solver
from geotherm.solvers import FiniteSolver

# temperature of the base of the lithosphere
T_lithosphere = u(1300,"degC")

def instant_subduction(underplated_section, **kwargs):
    # Find the base of the lithosphere
    d = underplated_section.depth(T_lithosphere)
    distance = u(100,"km")
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

    return stack_sections(
        forearc,
        underplated_section)

def stepped_subduction(underplated_section, **kwargs):
    """Method to subduct crust under a forearc
    modeled by Leigh Royden's model.
    """
    echo("Beginning to subduct slab")

    distance = kwargs.pop("distance", None)
    velocity = kwargs.pop("velocity", None)
    depth = kwargs.pop("depth", None)

    # Thickness of foreland lithosphere
    # at the time of subduction
    # Presumably, foreland in this case refers
    # to the lower plate of the thrust advancing
    # into the subduction zone
    # The Royden model assumes that the foreland
    # is in thermal equilibrium, and the lithospheric
    # depth is being maintained, which is likely a
    # reasonable approximation for the timescales involved.
    lithosphere_depth = underplated_section.depth(T_lithosphere)

    echo("Depth of the base of the "
        "lithosphere at the time of "
        "subduction:{0:.2f}".format(lithosphere_depth))

    echo("Subduction velocity: {}".format(velocity))

    dip = N.arctan(depth/distance).to("degrees")
    echo("Dip of subduction zone: {}".format(dip))

    # distance along subduction channel
    sub_distance = N.sqrt(distance**2+depth**2)

    duration = (sub_distance/velocity).to("Myr")

    echo("Duration of subduction: {}".format(duration))

    royden = forearc_solver(
        l=lithosphere_depth.into("m"),
        v=velocity.into("m/s"),
        Tm =T_lithosphere.into("degC"))

    def on_step(solver, **kwargs):
        """ Function to change finite solver
            boundary conditions at each step
        """
        step = kwargs.pop("step")
        steps = kwargs.pop("steps")
        completion = (step+1)/steps
        print(completion)

        sz_depth = depth*completion

        # Temperature at the subduction
        # interface
        T = royden(
            (distance*completion).into("m"),
            sz_depth.into("m"), # Depth of interest
            sz_depth.into("m")) # Depth of subduction interface

        T = u(T,"degC")

        solver.set_constraints(upper=T)

    solver = FiniteSolver(underplated_section)

    underplated_section = solver.final_section(
        duration=duration,
        step_function=on_step,
        **kwargs)

    forearc = forearc_section(
        thickness = depth,
        distance = distance,
        solver = royden)

    echo("Temperature at subduction interface "
         "at the time of underplating: {0} {1}"\
          .format(
              forearc.profile[-1],
              underplated_section.profile[0]))

    s = stack_sections(forearc, underplated_section)

    return duration, s
