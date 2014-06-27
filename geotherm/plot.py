from __future__ import division

import seaborn as sns
from matplotlib.pyplot import figure, subplots
import numpy as N

class Plotter(object):
    type = "single"
    def __init__(self, **plotting_options):
        self.options = plotting_options
        self.size = self.options.pop("figsize", (10,10))
        self.title_prefix = self.options.pop("title", "")
        if self.title_prefix != "":
            self.title_prefix += ": "

    def initialize(self, solver):
        self.solver = solver
        self.fig = figure(figsize=self.size, facecolor="white")
        self.ax = self.fig.add_subplot(111)
        self.setup_axes()
        self.fig.show()

    def setup_axes(self):
        self.title = self.fig.suptitle(self.title_prefix+"0 years", fontsize=16)
        self.ax.invert_yaxis()
        self.ax.set_xlabel(u"Temperature: \u00b0C")
        self.ax.set_ylabel("Depth (m)")

        temp_range = self.options.pop("range",None)
        if temp_range: self.ax.set_xlim(temp_range)
        self._y = self.solver.mesh.cellCenters[0]
        self.solution, = self.ax.plot(self.solver.initial_values, self._y, '-')

    def plot_solution(self, time, solution):
        self.title.set_text(self.title_prefix+"{0:.4f}".format(time))
        self.solution.set_xdata(solution)
        self.fig.canvas.draw()


class ComparisonPlotter(Plotter):
    type = "paired"
    def __init__(self,comparison_function,**plotting_options):
        super(ComparisonPlotter,self).__init__(**plotting_options)
        self.comparison_function = comparison_function

    def initialize(self, solver):
        self.solver = solver
        self.fig, (self.ax,self.ax2) = subplots(
            1,2,
            sharey=True,
            figsize=self.size,
            facecolor="white")
        self.setup_axes()
        self.ax2.set_xlabel(u"Error: \u00b0C")
        self.comparison, = self.ax.plot(self.solver.initial_values, self._y, '-')
        self.residuals, = self.ax2.plot(N.zeros(len(self._y)),self._y,'-')
        self.fig.show()

    def plot_solution(self, time, solution):
        comparator = self.comparison_function(time)
        self.comparison.set_xdata(comparator)
        self.residuals.set_xdata(solution-comparator)
        self.ax2.relim()
        self.ax2.autoscale()
        super(ComparisonPlotter, self).plot_solution(time,solution)

