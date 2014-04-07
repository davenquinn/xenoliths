#!/usr/bin/env python
from __future__ import division, print_function
import fipy as F
import numpy as N
import IPython

from .base import BaseSolver
from ..units import unit, u

class SimpleFiniteSolver(BaseSolver):
    """Explicit finite differentiation for one-layer 1d materials"""

    def __init__(self, layer, **kwargs):
        super(SimpleFiniteSolver,self).__init__(**kwargs)
        try:
            layers = layer.layers
            if len(layers) == 1:
                self.layer = layers[0]
            else:
                arg = self.__class__.__name__+" can be initialized only from a single layer or a section containing only one layer."
                raise ArgumentError(arg)
        except AttributeError:
            self.layer = layer

        self.material = self.layer.material
        self.depth = self.layer.thickness
        self.dy = self.layer.grid_spacing
        self.ny = int((self.depth/self.dy).into("dimensionless"))
        self.mesh = F.Grid1D(nx=self.ny, dx=self.dy.into("m"))

        t_min,t_max = (i.into("kelvin") for i in (self.T_surface, self.T_max))

        self.initial_values = [t_max]*self.ny

        self.var = F.CellVariable(name="Temperature", mesh=self.mesh, value=self.initial_values)
        self.var.constrain(t_min, self.mesh.facesLeft)
        self.var.constrain(t_max, self.mesh.facesRight)
        coefficient = self.material.diffusivity.into("m**2/s")
        self.equation = F.TransientTerm() == F.DiffusionTerm(coeff=coefficient)

    def fractional_timestep(self, duration):
        ts = self.stable_timestep()
        print(ts.to("year"))
        n_steps = int(N.ceil((duration/ts).to_base_units()))
        return duration/n_steps, n_steps

    def stable_timestep(self, padding=0):
        """Calculates stable time step for explicit finite solving"""
        time_step = (1-padding)*self.dy**2 / (2 * self.material.diffusivity)
        return time_step

    def solve(self, steps=None, duration=None):
        if duration:
            time_step, steps = self.fractional_timestep(duration)
        elif steps:
            time_step = self.stable_timestep(0.05)
            duration = steps*time_step
        else:
            raise TypeError("either `steps` or `duration` argument must be provided")

        print("Duration: {0:.2e}".format(duration.to("year")))
        print("Number of steps: {0}\n".format(steps))

        for step in range(steps):
            simulation_time = step*time_step
            print(simulation_time.to("year"))
            yield simulation_time, N.array(self.var.value)
            soln = self.equation.solve(var=self.var,dt=time_step.into("seconds"))
