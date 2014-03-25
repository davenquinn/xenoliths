#!/usr/bin/env python
from __future__ import division
import IPython
import fipy as F
import numpy as N
from scipy.special import erf
import seaborn as sns

from geotherm.models import HalfSpace, MaterialModel
from geotherm.units import quantity
from geotherm.solvers import FiniteSolver

from matplotlib.pyplot import figure, subplots

def plot(solver, iterations, range=None):

    fig, axarr = subplots(1,2,sharey=True)
    ax0,ax1 = axarr
    ax0.invert_yaxis()
    if range: ax0.set_xlim(range)
    y = solver.mesh.cellCenters[0]

    line1, = ax0.plot(solver.initial_values, y, '-')
    line2, = ax0.plot(solver.initial_values, y, '-')
    diff, = ax1.plot([0]*len(y),y,'-')
    fig.show()

    for t,solution in solver.solve(iterations):
        analytic = solver.space_model._temperature(t,y)
        line1.set_xdata(solution)
        line2.set_xdata(analytic)
        diff.set_xdata(solution-analytic)
        ax1.relim()
        ax1.autoscale()
        fig.canvas.draw()
        yield solution

material = MaterialModel()
space = HalfSpace(material)
solver = FiniteSolver(space)

data = list(plot(solver,1000, range=(0,2000)))
