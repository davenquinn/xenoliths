from __future__ import division, print_function

import click
import fipy as F
import numpy as N
from warnings import warn
from .base import BaseFiniteSolver
from ...units import u, DimensionalityError
from ...models import Section

class AdvancedFiniteSolver(BaseFiniteSolver):
    def __init__(self, section, **kwargs):
        BaseFiniteSolver.__init__(self,section, **kwargs)

        if not hasattr(section,"layers"):
            # We need to convert a layer to section
            section = Section(section)

        self.section = section

        self.mesh = self.create_mesh()

        self.initial_values = self.section.profile.into("kelvin")
        self.var = F.CellVariable(
            name="Temperature",
            mesh=self.mesh,
            value=self.initial_values)

        if self.constraints is not None:
            self.set_constraints(*self.constraints)

        if type == "explicit":
            # Use stable timesteps if we're running explicit finite differences
            if self.time_step is not None:
                warn("For explicit finite differences, the "
                          "timestep is not user-adjustable")
            self.time_step = self.stable_timestep(0.05)

        self.create_coefficient()

        if self.type == "crank-nicholson":
            eqns = [self.create_equation(i) for i in ("implicit","explicit")]
            self.equation = sum(eqns)
        else:
            self.equation = self.create_equation(self.type)

    def set_constraints(self, upper=None, lower=None):
        # Constraint can be set to none if we don't want to change
        constraints = (new if new is not None else old
                for new,old in zip((upper,lower),self.constraints))
        faces = (self.mesh.facesLeft, self.mesh.facesRight)

        for val, face in zip(constraints,faces):
            try:
                self.var.constrain(val.into("K"), face) ## Constrain as temperature
            except DimensionalityError:
                v = val.into("W/m**2")
                self.var.faceGrad.constrain([v], face) ## Constrain as flux

    def create_coefficient(self):
        """A spatially varying diffusion coefficient"""
        arr = self.section.material_property("diffusivity").into("m**2/s")
        arr = N.append(arr, arr[-1])
        assert len(arr) == len(self.mesh.faceCenters[0])
        self.diffusion_coefficient = F.FaceVariable(mesh=self.mesh, value=arr)

    def radiogenic_heating(self):
        """Radiogenic heat production varying in space."""

        a, Cp, rho = (self.section.material_property(i)
            for i in ("heat_generation","specific_heat", "density"))
        if a.sum().magnitude == 0:
            return None

        arr = (a/Cp/rho).into("K/s")
        assert len(arr) == len(self.mesh.cellCenters[0])

        return F.CellVariable(mesh=self.mesh, value=arr)

    def create_equation(self, type="implicit"):
        if type == "implicit":
            DiffusionTerm = F.DiffusionTerm
        elif type == "explicit":
            DiffusionTerm = F.ExplicitDiffusionTerm
        else:
            m = "Must specify either explicit or implicit diffusion"
            raise ArgumentError(m)

        trans = F.TransientTerm()
        diff = DiffusionTerm(coeff=self.diffusion_coefficient)

        h = self.radiogenic_heating()
        if h is not None:
            diff += h
        return trans == diff

    def stable_timestep(self, padding=0):
        """Stable timestep for explicit diffusion"""
        d = self.section.material_property("diffusivity")
        s = self.section.cell_sizes
        arr = super(AdvancedFiniteSolver,self).stable_timestep(d,s,padding=padding)
        return arr.min()

    def value(self):
        return u(self.var.value,"K").to("degC")

    def __solve__(self, steps=None, duration=None, **kw):
        """ A private method that implements solving given the keyword combinations
            defined in the `solve_implicit`, `solve_explicit`, and `solve_crank_nicholson`
            methods.
        """

        plotter = kw.pop("plotter",self.plotter)
        step_function = kw.pop("step_function",self.step_function)
        time_step = kw.pop("time_step", self.time_step)

        if steps and duration:
            # If we have both of these, we ignore any timestep that is set
            time_step = duration/steps
        elif steps:
            duration = steps*time_step
        elif duration:
            # Adjust timestep to be divisible into timeline
            time_step, steps = self.fractional_timestep(duration, time_step)
        else:
            raise ArgumentError("Either `steps` or `duration` argument must be provided")

        print("Duration: {0:.2e}".format(duration.to("year")))
        print("Number of steps: {0}".format(steps))
        print("Step length: {0}".format(time_step))

        with click.progressbar(range(steps),length=steps) as bar:
            h = self.radiogenic_heating()
            for step in bar:
                simulation_time = step*time_step
                if plotter is not None:
                    plotter(simulation_time, (self.section.cell_centers, self.value()))
                if step_function is not None:
                    step_function(self,
                        simulation_time=simulation_time,
                        step=step, steps=steps)

                dt = time_step.into("seconds")
                self.equation.solve(
                    var=self.var,
                    dt=dt)
                sol = self.value()
                yield simulation_time, sol

    def steady_state(self):
        diff = F.DiffusionTerm(coeff=self.diffusion_coefficient)
        # Apply radiogenic heating if it exists
        h = self.radiogenic_heating()
        if h is not None:
            diff += h

        diff.solve(var = self.var)
        return Section(self.section.layers,
                profile=self.value())

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
