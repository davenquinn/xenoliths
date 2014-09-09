from __future__ import division, print_function

from IPython import embed
import fipy as F
import numpy as N
from .base import BaseFiniteSolver
from ...units import u, DimensionalityError

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
            faces = (self.mesh.facesLeft, self.mesh.facesRight)
            for val, face in zip(self.constraints,faces):
                try:
                    self.var.constrain(val.into("K"), face) ## Constrain as temperature
                except DimensionalityError:
                    v = val.into("W/m**2")
                    self.var.faceGrad.constrain([v], face) ## Constrain as flux

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
        """Stable timestep for explicit diffusion"""
        def gen():
            for layer in self.section.layers:
                d = layer.material.diffusivity
                s = layer.grid_spacing
                yield super(AdvancedFiniteSolver,self).stable_timestep(d,s,padding=padding)
        return min(s for s in gen())

    def solve_implicit(self, **kw):
        """Quick but inaccurate, using any number of steps you choose."""
        print("Solving implicit")
        kw["steps"] = kw.pop("steps",100)
        return self.__solve__(**kw)

    def solve_explicit(self, **kw):
        print("Solving explicit")
        if "duration" in kw:
            time_step, steps = self.fractional_timestep(duration)
            kw["steps"] = steps
        elif "steps" in kw:
            time_step = self.stable_timestep(0.05)
            kw["duration"] = kw["steps"]*time_step
        else:
            raise TypeError("either `steps` or `duration` argument must be provided")
        return self.__solve__(**kw)

    def __solve__(self, steps=None, duration=None, **kw):
        """ A private method that implements solving given the keyword combinations
            defined in the `solve_implicit`, `solve_explicit`, and `solve_crank_nicholson`
            methods.
        """

        print("Duration: {0:.2e}".format(duration.to("year")))
        print("Number of steps: {0}".format(steps))

        time_step = duration/steps

        plotter = self.setup_plotter(kw)

        for step in range(steps):
            simulation_time = step*time_step
            print(simulation_time.to("year"))
            sol = u(N.array(self.var.value),"K").to("degC")
            if plotter:
                plotter.plot_solution(simulation_time,sol)
            yield simulation_time, sol
            self.equation.solve(
                var=self.var,
                dt=time_step.into("seconds"))
        print("")

    def solve_crank_nicholson(self,duration=None,steps=10,plotter=None):
        pass

    def solution(self, duration, type="implicit", **kwargs):
        function = getattr(self, "solve_"+type)
        sol = function(duration=duration, **kwargs)
        item = None # hackish; bring variable scope out of loop
        for item in sol:
            pass
        return item[1]
