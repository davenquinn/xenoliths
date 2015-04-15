from __future__ import division, print_function
from ..base import BaseSolver
from ...plot import Plotter
from ...models.geometry import Section
from ...units import u
import fipy as F
import numpy as N

class BaseFiniteSolver(BaseSolver):
    defaults = dict(
        constraints = (u(i,"degC") for i in (25,1500)),
        time_step = None,
        type = "implicit",
        plotter = lambda t,sol: print(t.to("year"))
    )
    def __init__(self, section,**kwargs):
        super(BaseFiniteSolver, self).__init__(**kwargs)

    def fractional_timestep(self, duration, ts=None):
        """
        Tunes a timestep to evenly divide up period.
        If no timestep is provided, defaults to dividing
        the period into 100 parts.
        """
        if ts:
            n_steps = int(N.ceil((duration/ts).to_base_units()))
        else:
            n_steps = 100
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

    def setup_plotter(self, kwargs):
        plotter = kwargs.pop("plotter", Plotter)
        plotter = plotter(**kwargs.pop("plot_options",{}))
        if plotter: plotter.initialize(self)
        return plotter


    def solve(self, steps=None, duration=None, **kwargs):
        plotter = kwargs.pop("plotter", None)

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
            sol = u(N.array(self.var.value),"K").to("degC")
            if plotter is not None:
                plotter(sol)
            yield simulation_time, sol
            soln = self.equation.solve(
                var=self.var,
                dt=time_step.into("seconds"))
