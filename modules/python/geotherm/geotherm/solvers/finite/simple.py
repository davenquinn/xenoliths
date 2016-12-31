#!/usr/bin/env python
from __future__ import division, print_function
import fipy as F
import numpy as N
import IPython

from .base import BaseFiniteSolver
from ..oceanic import HalfSpaceSolver
from ...units import unit, u

class SimpleFiniteSolver(BaseFiniteSolver):
    """Explicit finite differentiation for one-layer 1d materials"""

    def __init__(self, layer, **kwargs):
        super(SimpleFiniteSolver,self).__init__(layer, **kwargs)
        try:
            layers = layer.layers
            if len(layers) == 1:
                self.layer = layers[0]
            else:
                arg = self.__class__.__name__+" can be initialized only from a single layer or a section containing only one layer."
                raise ArgumentError(arg)
        except AttributeError:
            self.layer = layer

        self.analytical_solver = HalfSpaceSolver(layer)

        self.material = self.layer.material
        self.depth = self.layer.thickness
        self.dy = self.layer.grid_spacing
        self.ny = int((self.depth/self.dy).into("dimensionless"))
        self.mesh = F.Grid1D(nx=self.ny, dx=self.dy.into("m"))

        t_min,t_max = (i.into("kelvin") for i in self.constraints)

        self.initial_values = N.empty(self.ny)
        self.initial_values.fill(t_max)

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

    def solve(self, steps=None, duration=None, plotter=None):
        if duration:
            time_step, steps = self.fractional_timestep(duration)
        elif steps:
            time_step = self.stable_timestep(0.05)
            duration = steps*time_step
        else:
            raise TypeError("either `steps` or `duration` argument must be provided")

        print("Duration: {0:.2e}".format(duration.to("year")))
        print("Number of steps: {0}\n".format(steps))

        if plotter: plotter.initialize(self)
        y = self.mesh.cellCenters[0]

        for step in range(steps):
            simulation_time = step*time_step
            print(simulation_time.to("year"))
            sol = u(N.array(self.var.value),"K").to("degC")
            analytical = self.analytical_solver._temperature(simulation_time,y)
            plotter.plot_solution(sol,analytical)
            yield simulation_time, sol
            soln = self.equation.solve(var=self.var,dt=time_step.into("seconds"))

    def solution(self, duration, **kwargs):
        sol = self.solve(duration=duration, **kwargs)
        item = None # hackish; bring variable scope out of loop
        for t,item in sol:
            pass
        return item
