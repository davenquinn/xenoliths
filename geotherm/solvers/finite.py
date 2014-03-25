#!/usr/bin/env python
from __future__ import division
import fipy as F
import numpy as N

from ..units import quantity

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

    def time_step(self):
        """Calculates stable time step for explicit finite solving"""
        time_step = 0.9 * self.dy**2 / (2 * self.material.diffusivity)
        print time_step
        return time_step

    def solve(self, steps=10, viewer=False):
        time_step = self.time_step()
        if viewer:
            view = F.Matplotlib1DViewer(vars=(self.var))
            view.plot()

        for step in range(steps):
            simulation_time = step*time_step
            print simulation_time.to("year")
            yield simulation_time, N.array(self.var.value)
            soln = self.equation.solve(var=self.var,dt=time_step.magnitude)
