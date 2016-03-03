# -*- coding:utf-8 -*-

from __future__ import print_function, division

import numpy as N
import seaborn.apionly as sns
from uncertainties import unumpy
import matplotlib as M
from chroma import Color
import yaml
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.pyplot import figure, subplots_adjust
from scipy.stats import norm, gaussian_kde
from xenoliths import app
from xenoliths.models import Sample
from xenoliths.thermometry.rare_earth import (
    ree_pyroxene, regress, temperature, rare_earths)

from data import load_data, ree_data, sample_colors
from helpers import scatter_options, label

with open('font-style.yaml') as f:
    style_object = yaml.load(f)
for k,v in style_object.items():
    M.rc(k,**v)

xv = N.arange(len(rare_earths))

do_offsets = False

with open('ree-disequilibrium.txt') as f:
    lines = (d.split() for d in f.readlines())
    for_removal = {d.pop(0):d for d in lines}

# Leave space for Praseodymium
Pr_ix = 4
xv[Pr_ix:] += 1

def plot_uncertain(ax, x,y, **kwargs):
    u = N.array([m.n for m in y])
    s = N.array([m.s for m in y])
    color = kwargs.pop('color',None)

    ax.fill_between(x,u-s,u+s,
        facecolor=color,
        edgecolor='none',
        alpha=0.2)
    ax.plot(x,u, color=color, **kwargs)

# Load data for non-REE temperatures.
data = load_data()

fig = figure(figsize=(7.5,4), dpi=300)
transFigure = fig.transFigure.inverted()

def line_between(ax1,ax2,T,T1,**kwargs):
    xLims = lambda ax: [ax.transAxes.transform([i,0])[0] for i in range(2)]

    t = ax1.transData.transform([0,T])[1]
    coords = [(a,t) for a in xLims(ax1)]

    t = ax2.transData.transform([0,T1])[1]
    coords += [(a,t) for a in xLims(ax2)]

    coords = [transFigure.transform(i) for i in coords]
    x_ = [i[0] for i in coords]
    y_ = [i[1] for i in coords]

    line = Line2D(x_,y_,transform=fig.transFigure, **kwargs)
    fig.lines.append(line)

def plot_DREE(axes, sample, annotate=True, uncertainties=True, offset=0):
    offs = offset
    ax,ax1 = axes
    X,Y = sample.X, sample.Y

    to_remove = for_removal[sample.id]
    # Index of elements to remove from regression
    ix = N.in1d(rare_earths,to_remove)
    res = sample.res
    fitted_coeff = res.params[0]
    T = sample.temperature

    title = u"{id}: {n:.0f}±{s:.0f} °C"\
        .format(
            id=sample.id,
            n=T.n,
            s=T.s)

    y = Y/X-273.15 + offs

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

    ax.annotate(sample.id, (-0.5,T.n+offs), (-10, 0),
        xycoords='data', textcoords='offset points',
        va='center', ha='right', color=sample.color)

    # Plot probability density function
    s = res.bse[0] # B-hat standard estimator
    x = N.linspace(-3*s,3*s,100)
    P = norm.pdf(x,0,s)
    ax1.fill_betweenx(x+T.n,0,P,facecolor=sample.color, alpha=0.3, zorder=-10)
    ax1.plot(P,x+T.n, color=sample.color)

    linekws = dict(color=sample.color, linewidth=2, alpha=0.3)
    line_between(ax,ax1,T.n+offs,T.n, **linekws)

with app.app_context():
    gs = GridSpec(1, 3, width_ratios=[6, 1, 6])
    #gs.update(left=0.3, wspace=0.05)

    ax = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1])
    # Axis for comparisons
    comp_ax = fig.add_subplot(gs[2], sharey=ax1)

    ax1.invert_xaxis()

    if do_offsets:
        _ = 2400
    else:
        _ = 1500

    ax.set_ylim([800,_])
    ax1.set_ylim([900,1125])

    samples = (Sample.query
        .filter_by(xenolith=True)
        .order_by(Sample.id)
        .all())
    for s in samples:
        to_remove = for_removal[s.id]
        # Index of elements to remove from regression
        ix = N.in1d(rare_earths,to_remove)

        s.X,s.Y = ree_pyroxene(s, 1.5) # Pressure in GPa
        s.res = regress(s.X[~ix],s.Y[~ix])
        s.temperature = temperature(s.res)

    d = sorted(samples, key=lambda s: s.res.params[0])

    offsets = [0,175,None,160,None,350]

    offs = 0
    for o,sample in zip(offsets,d):
        if o is None:
            o = 200
        offs += o
        if not do_offsets: offs = 0

        plot_DREE((ax,ax1), sample, annotate=False, offset=offs)


    kw = dict(
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax.transAxes)

    ax.text(0.05, 1, r"Equilibrium T$_\mathrm{REE}$",**kw)
    ax.text(0.05, 0.95,u"100 \u00b0C increments, offset for clarity",
        size='smaller', color='#888888', **kw)

    ticks = xv
    ax.set_xlim([ticks[0]-0.5,ticks[-1]+0.5])
    ax.xaxis.set_ticks(ticks)
    ax.xaxis.set_ticklabels(rare_earths)

    ax.xaxis.get_ticklabels()[-1].set_color('#888888')
    ax.yaxis.set_ticklabels([])

    ax1.yaxis.tick_right()
    ax1.xaxis.set_ticks([])

    ax1.text(1.05, 1, u"T (\u00b0C)",
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax1.transAxes)

    data = {d['id']: d for d in data}
    # Comparison axis

    for sample in samples:
        temps = data[sample.id]
        ta98 = temps['core']['ta98']['sep']

        n = 1e4

        choice = N.random.choice(ta98,size=n)
        x = unumpy.nominal_values(choice)
        x += unumpy.std_devs(choice)*N.random.randn(n)
        # Plot probability density function
        res = sample.res
        _ = res.params[0]-273.15
        s = res.bse[0] # B-hat standard estimator
        y = s*N.random.randn(n) + _
        comp_ax.plot(x,y,
            marker='.',
            linestyle='none',
            color=sample.color,
            alpha=0.01,
            rasterized=True)

        comp_ax.set_rasterization_zorder(-10)

    comp_ax.yaxis.set_ticks([950,1000,1050,1100])

    comp_ax.autoscale(False)
    a = [0,2000]
    comp_ax.plot(a,a, c="#cccccc", zorder=-20)


    sns.despine(ax=ax)
    sns.despine(ax=ax1,left=True,bottom=True, right=False)

    fig.savefig("build/pyx-dree.pdf",bbox_inches="tight", dpi=300)
