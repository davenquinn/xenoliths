from __future__ import division

import seaborn as sns
from matplotlib.pyplot import figure

class Plotter(object):
    def __init__(self, **plotting_options):
        self.options = plotting_options

    def initialize(self, solver):
        self.solver = solver
        self.fig = figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.invert_yaxis()
        self.ax.set_xlabel(u"Temperature: \u00b0C")
        self.ax.set_ylabel("Depth (m)")

        temp_range = self.options.pop("range",None)
        if temp_range: self.ax.set_xlim(temp_range)
        y = self.solver.mesh.cellCenters[0]
        self.solution, = self.ax.plot(self.solver.initial_values, y, '-')
        self.fig.show()

    def plot_solution(self,solution):
        self.solution.set_xdata(solution)
        self.fig.canvas.draw()
