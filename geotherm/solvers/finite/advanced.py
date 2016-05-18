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

        self._excess = None

        if not hasattr(section,"layers"):
            # We need to convert a layer to section
            section = Section(section)

        self.section = section

        self.mesh = self.create_mesh()

        self.initial_values = self.section.profile.into("kelvin")
        self.var = F.CellVariable(
            name="Temperature",
            mesh=self.mesh,
            value=self.initial_values,
            hasOld=(self.type=='crank-nicholson'))

        self._exterior_flux = 0
        self.create_coefficient()

        if self.constraints is not None:
            self.set_constraints(*self.constraints)

        if self.type == "explicit":
            # Use stable timesteps if we're running explicit finite differences
            if self.time_step is not None:
                warn("For explicit finite differences, the "
                          "timestep is not user-adjustable")
            self.time_step = self.stable_timestep(0.05)

        if self.type == "crank-nicholson":
            eqns = [self.create_equation(i) for i in ("implicit","explicit")]
            self.__implicit_equation = eqns[0]
            self.equation = sum(eqns)
        else:
            self.equation = self.create_equation(self.type)

    def constrain(self, upper=None, lower=None):
        # Constraint can be set to none if we don't want to change
        constraints = (new if new is not None else old
                for new,old in zip((upper,lower),self.constraints))
        faces = (self.mesh.facesLeft, self.mesh.facesRight)
        indexes = [0,-1]

        self._exterior_flux = 0

        for val, index, face in zip(constraints,indexes,faces):
            if val is None:
                continue
            try:
                self.var.constrain(val.into("K"), face) ## Constrain as temperature
            except DimensionalityError:
                # Fixed flux boundary condition
                # flux density
                v = val.into("W/m^2")

                flux = F.FaceVariable(
                    self.mesh,'exterior_flux',
                    value=v)

                self._exterior_flux += (self.mesh.exteriorFaces[index]*flux).divergence

            except AttributeError:
                pass

    # Legacy callable
    set_constraints = constrain

    def create_coefficient(self):
        """A spatially varying diffusion coefficient"""
        arr = self.section.material_property("diffusivity").into("m**2/s")
        arr = N.append(arr, arr[-1])
        assert len(arr) == len(self.mesh.faceCenters[0])
        self.diffusion_coefficient = F.FaceVariable(mesh=self.mesh, value=arr)

    @property
    def excess_heating(self):
        return self._excess
    @excess_heating.setter
    def excess_heating(self, val):
        """
        Similar to radiogenic heat production, but not
        based on the material properties of the forearc.
        """
        if val == 0:
            v = None
        else:
            v = F.CellVariable(
                mesh=self.mesh,
                value=val.into('K/s'))
        self._excess = v

    def radiogenic_heating(self):
        """Radiogenic heat production varying in space."""

        a, Cp, rho = (self.section.material_property(i)
            for i in ("heat_generation","specific_heat", "density"))
        if a.sum().magnitude == 0:
            return None

        arr = (a/Cp/rho).into("K/s")
        assert len(arr) == len(self.mesh.cellCenters[0])

        return F.CellVariable(mesh=self.mesh, value=arr)

    def create_equation(self, type='implicit'):
        trans = F.TransientTerm()
        diff = self.diffusion_term(type)
        return trans == diff

    def stable_timestep(self, padding=0):
        """Stable timestep for explicit diffusion"""
        d = self.section.material_property("diffusivity")
        s = self.section.cell_sizes
        arr = super(AdvancedFiniteSolver,self).stable_timestep(d,s,padding=padding)
        return arr.min()

    def value(self):
        return u(self.var.value,"K").to("degC")

    def __do_step(self, dt):
        if self.type == 'crank-nicholson':
            self.var.updateOld()
            self.equation.sweep(var=self.var,dt=dt)
            self.__implicit_equation.sweep(var=self.var,dt=dt)
        else:
            self.equation.solve(var=self.var,dt=dt)

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
                self.__do_step(dt)
                sol = self.value()
                yield simulation_time, sol

    def diffusion_term(self, type="implicit"):
        if type == "implicit":
            DiffusionTerm = F.DiffusionTerm
        elif type == "explicit":
            DiffusionTerm = F.ExplicitDiffusionTerm
        else:
            m = "Must specify either explicit or implicit diffusion"
            raise ArgumentError(m)

        diff = DiffusionTerm(coeff=self.diffusion_coefficient)
        # Apply radiogenic heating if it exists
        h = self.radiogenic_heating()
        if h is not None:
            diff += h
        # Add exterior fluxes
        diff += self._exterior_flux
        return diff

    def steady_state(self):
        D = self.diffusion_term()
        D.solve(var = self.var)
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
