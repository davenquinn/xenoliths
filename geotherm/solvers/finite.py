#!/usr/bin/env python
from __future__ import division
import fipy as F
import numpy as N

from ..units import unit

class FiniteSolver(object):
    """Explicit finite differentiation"""
    def __init__(self, space_model):
        self.space_model = space_model
        self.material = space_model.material
        self.depth = quantity(1e5,"m") #m
        self.dy = quantity(100,"m")
        self.ny = self.depth/self.dy
        self.mesh = F.Grid1D(nx=self.ny.magnitude, dx=self.dy.magnitude)

        t_min,t_max = (getattr(self.space_model,i).to("kelvin").magnitude for i in ("T_surface","T_max"))

        self.initial_values = [t_max]*int(self.ny.magnitude)

        self.var = F.CellVariable(name="Temperature", mesh=self.mesh, value=self.initial_values)
        self.var.constrain(t_min, self.mesh.facesLeft)
        self.var.constrain(t_max, self.mesh.facesRight)
        self.equation = F.TransientTerm() == F.DiffusionTerm(coeff=self.material.diffusivity.magnitude)

    def fractional_timestep(self, duration):
        ts = self.stable_timestep()
        n_steps = int(N.ceil((duration/ts).to("year")))
        return duration/n_steps, n_steps

    def stable_timestep(self, padding=0):
        """Calculates stable time step for explicit finite solving"""
        time_step = (1-padding)*self.dy**2 / (2 * self.material.diffusivity)
        return time_step

    def solve(self, steps=None, duration=None):
        if duration:
            time_step, steps = self.fractional_timestep(duration)
        elif steps:
            time_step = self.stable_timestep(0.9)
        else:
            raise TypeError("either `steps` or `duration` argument must be provided")

        for step in range(steps):
            simulation_time = step*time_step
            print simulation_time.to("year")
            yield simulation_time, N.array(self.var.value)
            soln = self.equation.solve(var=self.var,dt=time_step.magnitude)
