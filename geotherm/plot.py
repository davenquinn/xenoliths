from __future__ import division, print_function

import seaborn as sns
from matplotlib.pyplot import figure, subplots
import numpy as N

class Plotter(object):
    type = "single"
    def __init__(self, **plotting_options):
        self.options = plotting_options
        self.title_prefix = self.options.pop("title", "")
        if self.title_prefix != "":
            self.title_prefix += ": "

        self.fig = figure(
            figsize=self.options.pop("figsize", (10,10)),
            facecolor="white")
        self.solution = None
        self.ax = self.fig.add_subplot(111)
        self.setup_axes()

    def setup_axes(self):
        self.title = self.fig.suptitle(self.title_prefix+"0 years", fontsize=16)
        self.ax.invert_yaxis()
        self.ax.set_xlabel(u"Temperature: \u00b0C")
        self.ax.set_ylabel("Depth (m)")

        temp_range = self.options.pop("range",None)
        if temp_range: self.ax.set_xlim(temp_range)

    def __call__(self, time, section):
        if not self.solution:
            self.solution, = self.ax.plot(
                section[1], section[0], '-')
            self.fig.show()
        else:
            self.solution.set_ydata(section[0])
            self.solution.set_xdata(section[1])
        self.title.set_text(self.title_prefix+"{0:.4f}".format(time))
        print(time)
        self.fig.canvas.draw()

