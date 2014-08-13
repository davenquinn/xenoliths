from __future__ import division, print_function
from ..base import BaseSolver
from ...models.geometry import Section
from ...units import u
import fipy as F
import numpy as N

class BaseFiniteSolver(BaseSolver):
    defaults = dict(
        constraints = (u(i,"degC") for i in (25,1500))
    )
    def __init__(self, section,**kwargs):
        super(BaseFiniteSolver, self).__init__(**kwargs)

    def fractional_timestep(self, duration):
        ts = self.stable_timestep()
        print(ts.to("year"))
        n_steps = int(N.ceil((duration/ts).to_base_units()))
        return duration/n_steps, n_steps

    def create_mesh(self):
        kwargs = dict(
            nx = self.section.n_cells,
            dx = self.section.cell_sizes.into("m"))
        return F.Grid1D(**kwargs)

    def stable_timestep(self, diffusivity, cell_spacing, padding=0):
        """Calculates stable time step for explicit finite solving"""
        time_step = (1-padding)*cell_spacing**2 / (2*diffusivity)
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

        if plotter:
            plotter.initialize(self)

        for step in range(steps):
            simulation_time = step*time_step
            print(simulation_time.to("year"))
            sol = u(N.array(self.var.value),"K").to("degC")
            if plotter:
                plotter.plot_solution(sol)
            yield simulation_time, sol
            soln = self.equation.solve(
                var=self.var,
                dt=time_step.into("seconds"))
