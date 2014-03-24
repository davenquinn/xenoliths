#!/usr/bin/env python
from __future__ import division
import IPython
import fipy as F
import numpy as N
from scipy.special import erf

from geotherm.models import HalfSpace, MaterialModel
from geotherm.units import quantity
from geotherm.finite import FiniteSolver

from matplotlib.pyplot import figure

def plot(solver, iterations):
    fig = figure()
    ax = fig.add_subplot(111)
    line = None
    IPython.embed()
    for sol in solver.solve(iterations):
        if line == None:
            y = solver.mesh.cellCenters[0]
            line, = ax.plot(sol, y, 'r-') # Returns a tuple of line objects, thus the comma
            fig.show()
        else:
            line.set_xdata(sol)
            fig.canvas.draw()
        yield sol

material = MaterialModel()
space = HalfSpace(material)
solver = FiniteSolver(space)
data = list(plot(solver,100))
