# -*- coding:utf-8 -*-

from __future__ import print_function, division

import numpy as N
from matplotlib.pyplot import subplots
from xenoliths import app
from xenoliths.models import Sample
from xenoliths.thermometry.rare_earth import (
    ree_pyroxene, regress, temperature, rare_earths)

xv = N.arange(len(rare_earths))

# Leave space for Praseodymium
# Pr_ix = 4
# xv[Pr_ix:] += 1

def plot_uncertain(ax, x,y, **kwargs):
    u = N.array([m.n for m in y])
    s = N.array([m.s for m in y])
    color = kwargs.pop('color',None)

    ax.fill_between(x,u-s,u+s,
        facecolor=color,
        edgecolor='none',
        alpha=0.2)
    ax.plot(x,u, color=color, **kwargs)

def plot_DREE(ax, sample, annotate=True, uncertainties=True):
    X,Y = ree_pyroxene(sample, 1.5) # Pressure in GPa
    res = regress(X,Y)
    fitted_coeff = res.params[0]

    T = temperature(res)

    title = u"{id}: {n:.0f}±{s:.0f} °C"\
        .format(
            id=sample.id,
            n=T.n,
            s=T.s)

    y = Y/X-273.15
    kwargs = dict(
        color=sample.color)
    if uncertainties:
        plot_uncertain(ax,xv,y,**kwargs)
    else:
        n = N.array([m.n for m in y])
        ax.plot(xv,n,'-',**kwargs)
    T = res.params[0]-273.15 * N.ones_like(xv)

    ax.plot(xv,T,"-",color=sample.color, linewidth=0.5, zorder=-5)


    res = regress(X,Y,hree_only=True)
    T = res.params[0]-273.15 * N.ones_like(xv)
    ax.plot(xv,T,":",color=sample.color, linewidth=0.5, zorder=-5)

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

    ticks = xv
    ax.set_xlim([ticks[0]-0.5,ticks[-1]+0.5])
    ax.xaxis.set_ticks(ticks)
    ax.xaxis.set_ticklabels(rare_earths)

    fig.savefig("build/pyx-dree.pdf",bbox_inches="tight")
