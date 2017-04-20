from __future__ import division

import numpy as N
import matplotlib
from matplotlib import pyplot as P

from xenoliths import app
from xenoliths.thermometry.rare_earth.plot import ree_temperature
from xenoliths.thermometry.results import (
    xenoliths, core_temperatures, Ca_OPX_Corr, Taylor1998)

from helpers import label, scatter_options

matplotlib.rcParams.update({'font.size': 8})

with app.app_context():
    samples = xenoliths()
    colors = [s.color for s in samples]

    ree = [ree_temperature(s,
            pressure=1.5,
            uncertainties=True,
            # Use only HREEs for CK-4 because this
            # exhibits extreme disequilibrium
            hree_only=(s.id == 'CK-4'))
            for s in samples]

    methods = (Taylor1998,Ca_OPX_Corr)
    temps = tuple([N.array(core_temperatures(s,method=method))
        for s in samples] for method in methods)

fig, axes = P.subplots(3,1,figsize=(4,6), sharex=True)
fig.subplots_adjust(hspace=0)

def plot(ax, y, x):
    n = [i.n for i in y]
    nx = [i.mean() for i in x]
    for i,(x_,yv) in enumerate(zip(x,y)):
        y_ = [yv.n]*len(x_)
        ax.errorbar(yv.n,x_.mean(),
                xerr=yv.s,
            linestyle="None",
            color='#cccccc')
        ax.plot(
            [yv.n,yv.n],
            [x_.min(),x_.max()],
            color='#cccccc')
        ax.scatter(y_,x_,zorder=5, s=20,
            **scatter_options(colors[i]))

labels = ('TA98','Ca-OPX')

for ax,l,T in zip(axes, labels, temps):

    plot(ax, ree,T)
    ax.set_ylabel(label(l))

for i,ax in enumerate(axes):
    # Draw unity line
    ax.autoscale(False)
    a = [0,2000]
    ax.plot(a,a, c="#cccccc", zorder=-5)

    if i == 0:
        ax.set_ylim((910,1120))
    else:
        ax.set_ylim((970,1120))


ax.set_xlabel(label("REE"))

fig.savefig("build/ree-temperatures.pdf", bbox_inches='tight')
