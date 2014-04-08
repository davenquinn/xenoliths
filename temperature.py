#!/usr/bin/env python
from __future__ import division, print_function
import IPython
import fipy as F
import numpy as N
from scipy.special import erf
import seaborn as sns

from geotherm.models.material import Material
from geotherm.models.geometry import Layer
from geotherm.units import unit, u
from geotherm.solvers import HalfSpaceSolver
from geotherm.solvers.finite import SimpleFiniteSolver

from matplotlib.pyplot import figure, subplots

def plot(finite, analytic, **kwargs):
    """
    Takes arguments
    ..range
    """
    fig, axarr = subplots(1,2,sharey=True)
    ax0,ax1 = axarr
    ax0.invert_yaxis()

    range = kwargs.pop("range",None)
    if range:
        ax0.set_xlim(range)

    y = finite.mesh.cellCenters[0]

    line1, = ax0.plot(finite.initial_values, y, '-')
    line2, = ax0.plot(finite.initial_values, y, '-')
    diff, = ax1.plot([0]*len(y),y,'-')
    fig.show()

    for t,solution in finite.solve(**kwargs):
        a = analytic._temperature(t,y)
        line1.set_xdata(solution)
        line2.set_xdata(a)
        diff.set_xdata(solution-a)
        ax1.relim()
        ax1.autoscale()
        fig.canvas.draw()
        yield solution

layer = oceanic_mantle.to_layer(u(100,"km"))
finite = SimpleFiniteSolver(layer)
analytic = HalfSpaceSolver(layer)


time = u(3,"Myr")

data = list(plot(finite,analytic,duration=time,range=(0,2000)))
