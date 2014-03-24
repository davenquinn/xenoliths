#!/usr/bin/env python
from __future__ import division
import fipy as F

from ..units import quantity

class FiniteSolver(object):
    """Explicit finite differentiation"""
    def __init__(self, space_model):
        self.space_model = space_model
        self.material = space_model.material
        self.depth = quantity(1e5,"m") #m
        self.dy = quantity(100,"m")
        ny = self.depth/self.dy
        self.mesh = F.Grid1D(nx=ny.magnitude, dx=self.dy.magnitude)

        t_min,t_max = (getattr(self.space_model,i).to("kelvin").magnitude for i in "T_surface", "T_max")

        initialValues = [t_max]*int(ny.magnitude)

        self.var = F.CellVariable(name="Temperature", mesh=self.mesh, value=initialValues)
        self.var.constrain(t_min, self.mesh.facesRight)
        self.var.constrain(t_max, self.mesh.facesLeft)
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
            soln = self.equation.solve(var=self.var,
                      dt=time_step.magnitude)
            if viewer: view.plot()
            yield self.var.value
