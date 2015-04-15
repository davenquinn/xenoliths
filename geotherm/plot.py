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
        print("Initializing plotter.")
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

    def __call__(self, time, solution):
        self.title.set_text(self.title_prefix+"{0:.4f}".format(time))
        self.solution.set_xdata(solution)
        print("Plotting solution")
        self.fig.canvas.draw()

