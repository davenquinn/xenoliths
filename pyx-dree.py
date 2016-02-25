# -*- coding:utf-8 -*-

from __future__ import print_function, division

import numpy as N
from matplotlib.gridspec import GridSpec
from matplotlib.pyplot import figure
from scipy.stats import norm
from xenoliths import app
from xenoliths.models import Sample
from xenoliths.thermometry.rare_earth import (
    ree_pyroxene, regress, temperature, rare_earths)

xv = N.arange(len(rare_earths))

with open('ree-disequilibrium.txt') as f:
    lines = (d.split() for d in f.readlines())
    for_removal = {d.pop(0):d for d in lines}

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

def plot_DREE(axes, sample, annotate=True, uncertainties=True):
    ax,ax1 = axes
    X,Y = ree_pyroxene(sample, 1.5) # Pressure in GPa

    to_remove = for_removal[sample.id]
    # Index of elements to remove from regression
    ix = N.in1d(rare_earths,to_remove)
    res = regress(X[~ix],Y[~ix])
    fitted_coeff = res.params[0]
    T = temperature(res)

    title = u"{id}: {n:.0f}±{s:.0f} °C"\
        .format(
            id=sample.id,
            n=T.n,
            s=T.s)

    y = Y/X-273.15

    kwargs = dict(
        color=sample.color,
        linewidth=1)

    n = N.array([m.n for m in y])
    if uncertainties:
        plot_uncertain(ax,xv,y,**kwargs)
    else:
        ax.plot(xv,n,'-',**kwargs)

    # Plot filled and open circles
    kws = dict(edgecolor=sample.color, marker='o', zorder=10)
    ax.scatter(xv[ix],n[ix], color='#ffffff', **kws)
    ax.scatter(xv[~ix],n[~ix],color=sample.color,**kws)

    ax.axhline(y=T.n, label=sample.id, color=sample.color)


    # Plot probability density function
    s = res.bse[0]
    offs = fitted_coeff-273.15
    x = N.linspace(-3*s,3*s,100)
    P = norm.pdf(x,0,s)
    ax1.plot(P,x+offs, color=sample.color)


with app.app_context():
    fig = figure(figsize=(6.5,5))
    gs = GridSpec(1, 2, width_ratios=[6, 1])
    ax = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharey=ax)

    samples = (Sample.query
        .filter_by(xenolith=True)
        .order_by(Sample.id)
        .all())

    for sample in samples:
        plot_DREE((ax,ax1), sample, annotate=False)

    ax.set_ylabel(u"T (\u00b0C)")

    ticks = xv
    ax.set_xlim([ticks[0]-0.5,ticks[-1]+0.5])
    ax.xaxis.set_ticks(ticks)
    ax.xaxis.set_ticklabels(rare_earths)

    fig.savefig("build/pyx-dree.pdf",bbox_inches="tight")
