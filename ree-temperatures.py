from __future__ import division

import numpy as N
import matplotlib
from matplotlib import pyplot as P
from chroma import Color

from xenoliths import app
from xenoliths.thermometry.rare_earth.plot import ree_temperature
from xenoliths.thermometry.results import xenoliths, core_temperatures

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

    ta98 = [N.array(core_temperatures(s))
            for s in samples]

fig, ax = P.subplots(figsize=(4,3))

def plot(x,y):
    n = [i.n for i in y]
    nx = [i.mean() for i in x]
    for i,(x_,yv) in enumerate(zip(x,y)):
        y_ = [yv.n]*len(x_)
        ax.errorbar(x_.mean(),yv.n,
                yerr=yv.s,
            linestyle="None",
            color='#cccccc')
        ax.plot(
            [x_.min(),x_.max()],
            [yv.n,yv.n],
            color='#cccccc')
        ax.scatter(x_,y_,zorder=5, s=20,
            **scatter_options(colors[i]))

plot(ta98,ree)
ax.set_xlabel(label("TA98"))
ax.set_ylabel(label("REE"))

#for x,y,s in zip(ta98,ree,samples):
#    ax.annotate(s.id, (x,y), xytext=(-5,5), textcoords="offset points")

ax.autoscale(False)
a = [0,2000]
ax.plot(a,a, c="#cccccc", zorder=-5)

fig.savefig("build/ree-temperatures.pdf", bbox_inches='tight')

