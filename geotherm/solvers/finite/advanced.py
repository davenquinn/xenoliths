from __future__ import division, print_function

import fipy as F
import numpy as N
from warnings import warn
from .base import BaseFiniteSolver
from ...units import u, DimensionalityError
from ...models import Section

class AdvancedFiniteSolver(BaseFiniteSolver):
    def __init__(self, section, **kwargs):
        BaseFiniteSolver.__init__(self,section, **kwargs)
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

        if type == "explicit":
            # Use stable timesteps if we're running explicit finite differences
            if self.time_step is not None:
                warn("For explicit finite differences, the"
                          "timestep is not user-adjustable")
            self.time_step = self.stable_timestep(0.05)

        self.create_coefficient()
        self.radiogenic_heat()

        if self.type == "crank-nicholson":
            eqns = [self.create_equation(i) for i in ("implicit","explicit")]
            self.equation = sum(eqns)
        else:
            self.equation = self.create_equation(self.type)

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

    def radiogenic_heat(self):
        """Radiogenic heat production varying in space."""
        def build_array():
            for layer in self.section.layers:
                m = layer.material
                coeff = m.heat_generation/m.specific_heat/m.density
                a = N.empty(layer.n_cells)
                a.fill(coeff.into("K/s"))
                yield a
        arr = N.concatenate(tuple(build_array()))
        arr = N.append(arr, arr[-1])
        assert len(arr) == len(self.mesh.faceCenters[0])
        self.heat_generation = F.FaceVariable(mesh=self.mesh, value=arr)

    def create_equation(self, type="implicit"):
        if type == "implicit":
            DiffusionTerm = F.DiffusionTerm
        elif type == "explicit":
            DiffusionTerm = F.ExplicitDiffusionTerm
        else:
            m = "Must specify either explicit or implicit diffusion"
            raise ArgumentError(m)

        trans = F.TransientTerm()
        diff = DiffusionTerm(coeff=self.diffusion_coefficient)\
                + self.heat_generation.divergence
        return trans == diff

    def stable_timestep(self, padding=0):
        """Stable timestep for explicit diffusion"""
        def gen():
            for layer in self.section.layers:
                d = layer.material.diffusivity
                s = layer.grid_spacing
                yield super(AdvancedFiniteSolver,self).stable_timestep(d,s,padding=padding)
        return min(s for s in gen())

    def __solve__(self, steps=None, duration=None, **kw):
        """ A private method that implements solving given the keyword combinations
            defined in the `solve_implicit`, `solve_explicit`, and `solve_crank_nicholson`
            methods.
        """

        print("Duration: {0:.2e}".format(duration.to("year")))
        print("Number of steps: {0}".format(steps))

        default = lambda t,sol: print(t.to("year"))
        plotter = kw.pop("plotter",default)

        time_step = kw.pop("time_step", self.time_step)

        if steps and duration:
            # If we have both of these, we ignore any timestep that is set
            time_step = duration/steps
        elif steps:
            duration = steps*time_step
        elif duration:
            # Adjust timestep to be divisible into 
            time_step, steps = self.fractional_timestep(duration, time_step)
            kw["steps"] = steps
        else:
            raise ArgumentError("Either `steps` or `duration` argument must be provided")

        for step in range(steps):
            simulation_time = step*time_step
            sol = u(N.array(self.var.value),"K").to("degC")
            if plotter is not None:
                plotter(simulation_time,sol)
            yield simulation_time, sol
            self.equation.solve(
                var=self.var,
                dt=time_step.into("seconds"))

    def solution(self, duration, **kwargs):
        sol = self.__solve__(duration=duration, **kwargs)
        item = None # hackish; bring variable scope out of loop
        for item in sol:
            pass
        return item[1]

    def final_section(self, *args, **kwargs):
        return Section(self.section.layers,
            profile=self.solution(*args,**kwargs))

    __call__ = final_section
