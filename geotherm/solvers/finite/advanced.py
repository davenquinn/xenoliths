from __future__ import division, print_function

from IPython import embed
import fipy as F
import numpy as N
from .base import BaseFiniteSolver
from ...units import u

class AdvancedFiniteSolver(BaseFiniteSolver):
    def __init__(self, section, **kwargs):
        super(AdvancedFiniteSolver, self).__init__(section, **kwargs)
        self.section = section
        self.mesh = self.create_mesh()

        self.initial_values = self.section.profile.into("kelvin")
        self.var = F.CellVariable(
            name="Temperature",
            mesh=self.mesh,
            value=self.initial_values)

        if self.constraints is not None:
            ## This implements only temperature constraints
            ## Will implement no-flux constraints if needed
            self.var.constrain(self.constraints[0].into("K"), self.mesh.facesLeft)
            self.var.constrain(self.constraints[1].into("K"), self.mesh.facesRight)

        self.create_coefficient()
        self.create_equation()

    def create_coefficient(self):
        """A spatially varying diffusion coefficient"""
        def build_array():
            for layer in self.section.layers:
                coeff = layer.material.diffusivity.into("m**2/s")
                a = N.empty(layer.n_cells)
                a.fill(coeff)
                yield a
        arr = N.concatenate(list(build_array()))
        arr = N.append(arr, arr[-1])
        assert len(arr) == len(self.mesh.faceCenters[0])
        self.diffusion_coefficient = F.FaceVariable(mesh=self.mesh, value=arr)

    def create_equation(self):
        trans = F.TransientTerm()
        diff = F.DiffusionTerm(coeff=self.diffusion_coefficient)
        self.equation = trans == diff

    def stable_timestep(self, padding=0):
        def gen():
            for layer in self.section.layers:
                d = layer.material.diffusivity
                s = layer.grid_spacing
                yield super(AdvancedFiniteSolver,self).stable_timestep(d,s,padding=padding)
        return min(s for s in gen())

    def solve_implicit(self, duration=None, steps=10, plotter=None):
        """Quick but inaccurate"""
        print("Solving implicit")
        time_step = duration/steps
        if plotter:
            plotter.initialize(self)

        for step in range(steps):
            simulation_time = step*time_step
            print(simulation_time.to("year"))
            sol = u(N.array(self.var.value),"K").to("degC")
            if plotter:
                plotter.plot_solution(sol)
            yield simulation_time, sol
            sol = self.equation.solve(
                var=self.var,
                dt=time_step.into("seconds"))

    def solve_crank_nicholson(self,duration=None,steps=10,plotter=None):
        pass
