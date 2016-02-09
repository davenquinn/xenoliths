# -*- coding:utf-8 -*-

from __future__ import print_function, division

import numpy as N
from matplotlib.pyplot import subplots
from xenoliths import app
from xenoliths.models import Sample
from xenoliths.thermometry.rare_earth import (
    ree_pyroxene, regress, temperature, rare_earths)

def plot_DREE(ax, sample, annotate=True):
    X,Y = ree_pyroxene(sample, 1.5) # Pressure in GPa
    res = regress(X,Y)
    fitted_coeff = res.params[0]

    T = temperature(res)

    title = u"{id}: {n:.0f}±{s:.0f} °C"\
        .format(
            id=sample.id,
            n=T.n,
            s=T.s)

    xv = N.arange(len(X))
    ax.plot(xv,Y/X-273.15, "-", color=sample.color, linewidth=2, zorder=5)
    T = res.params[0]-273.15 * N.ones_like(xv)
    ax.plot(xv,T,"-",color=sample.color)


    res = regress(X,Y,hree_only=True)
    T = res.params[0]-273.15 * N.ones_like(xv)
    ax.plot(xv,T,":",color=sample.color)

    return ax

with app.app_context():
    fig, ax = subplots(
            figsize=(6.5,5),
            sharey=True, sharex=True)
    samples = (Sample.query
        .filter_by(xenolith=True)
        .order_by(Sample.id)
        .all())

    for sample in samples:
        ax = plot_DREE(ax, sample, annotate=False)

    ax.set_ylabel(u"T (\u00b0C)")

    ax.xaxis.set_ticks(N.arange(len(rare_earths)))
    ax.xaxis.set_ticklabels(rare_earths)

    fig.savefig("build/pyx-dree.pdf",bbox_inches="tight")
