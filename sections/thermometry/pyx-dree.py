# -*- coding:utf-8 -*-

from __future__ import print_function, division

import numpy as N
import seaborn.apionly as sns
from paper.plot_style import update_axes, axis_labels
from uncertainties import unumpy
import matplotlib as M
import yaml
from collections import defaultdict
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.pyplot import figure, subplots_adjust
from scipy.stats import norm, gaussian_kde
from xenoliths import app, db
from xenoliths.models import Sample
from xenoliths.thermometry.rare_earth import (
    ree_pyroxene, regress, temperature, rare_earths)

from data import load_data, ree_data, sample_colors
from helpers import scatter_options, label
from contour_scatter import ScatterPlotter

with open('font-style.yaml') as f:
    style_object = yaml.load(f)
for k,v in style_object.items():
    M.rc(k,**v)

label_offsets = defaultdict(int)
label_offsets['CK-6'] = 5
label_offsets['CK-4'] = -5
label_offsets['CK-2'] = 7
label_offsets['CK-7'] = 5
label_offsets['CK-5'] = 0

xv = N.arange(len(rare_earths))

do_offsets = False

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

aspect_ratio = (7.5,3)
fig = figure(figsize=aspect_ratio, dpi=300)
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
    return N.array([x_,y_]).transpose()

def plot_DREE(axes, sample, annotate=True, uncertainties=True, offset=0):
    offs = offset
    ax,ax1 = axes
    X,Y = sample.X, sample.Y

    # Index of elements to remove from regression
    ix = N.in1d(rare_earths,sample.to_remove)
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
    kws = dict(edgecolor=sample.color, marker='o', zorder=10, s=10)
    ax.scatter(xv[ix],n[ix], color='#ffffff', **kws)
    ax.scatter(xv[~ix],n[~ix],color=sample.color,**kws)

    # Plot probability density function
    s = res.bse[0] # B-hat standard estimator
    x = N.linspace(-3*s,3*s,100)
    P = norm.pdf(x,0,s)
    ax1.fill_betweenx(x+T.n,0,P,facecolor=sample.color, alpha=0.3, zorder=-10)
    ax1.plot(P,x+T.n, color=sample.color, linewidth=1)

    linekws = dict(color=sample.color, linewidth=2, alpha=0.2)
    coords = line_between(ax,ax1,T.n+offs,T.n, **linekws)

    coords = coords[1:3]

    c = N.array(aspect_ratio)*coords
    tup  = c[1]-c[0]
    angle = 90-N.degrees(N.arctan2(*tup))
    center = coords.mean(axis=0)

    ax.annotate(sample.id, center, (-3, label_offsets[sample.id]),
        fontsize=10,
        rotation=angle,
        xycoords='figure fraction',
        textcoords='offset points',
        va='center', ha='center', color=sample.color,
        zorder=20)

with app.app_context():

    gs_left = M.gridspec.GridSpec(1, 1)
    gs_right = M.gridspec.GridSpec(1, 2, width_ratios=[1,6], wspace=0.05)
    gs_left.update(right=0.55, bottom=0.1,top=0.99)
    gs_right.update(left=0.6, bottom=0.1, top=0.99)

    # add plots to the nested structure
    ax = fig.add_subplot(gs_left[0])
    ax1 = fig.add_subplot(gs_right[0])
    comp_ax = fig.add_subplot(gs_right[1], sharey=ax1)

    ax1.invert_xaxis()

    if do_offsets:
        _ = 2400
    else:
        _ = 1500

    ylim2 = [900,1125]

    ax.set_ylim([800,_])
    ax1.set_ylim(ylim2)

    sample_ids = (db.session.query(Sample.id)
        .filter(Sample.xenolith==True)
        .order_by(Sample.id)
        .all())
    samples = [ree_data(id) for id, in sample_ids]

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

    if do_offsets:
        ax.text(0.05, 1, r"Equilibrium T$_\mathrm{REE}$",**kw)
        ax.text(0.05, 0.95,u"100 \u00b0C increments, offset for clarity",
            size='smaller', color='#888888', **kw)
        ax.yaxis.set_ticklabels([])

    ticks = xv
    ax.set_xlim([ticks[0]-0.5,ticks[-1]+0.5])
    ax.xaxis.set_ticks(ticks)
    ax.xaxis.set_ticklabels(rare_earths)

    ax.xaxis.get_ticklabels()[-1].set_color('#888888')
    ax1.xaxis.set_ticks([])

    data = {d['id']: d for d in data}
    # Comparison axis
    cxlim = [900,1100]
    scatter = ScatterPlotter(comp_ax, nx=40, ny=60,
        xrange=cxlim, yrange=ylim2, nlevels=15, color_exponent=0.8)
    for sample in samples:
        print(sample.id)
        temps = data[sample.id]
        ta98 = temps['core']['ta98']['sep']

        n = 10000

        choice = N.random.choice(ta98,size=n)
        x = unumpy.nominal_values(choice)
        x += unumpy.std_devs(choice)*N.random.randn(n)
        # Plot probability density function
        res = sample.res
        _ = res.params[0]-273.15
        s = res.bse[0] # B-hat standard estimator
        y = s*N.random.randn(n) + _
        #comp_ax.plot(x,y,
            # marker='.',
            # linestyle='none',
            # color=sample.color,
            # alpha=0.01,
            # rasterized=True)
        scatter(x,y,color=sample.color)

        comp_ax.set_rasterization_zorder(-10)

    comp_ax.yaxis.tick_right()
    comp_ax.yaxis.set_label_position("right")
    comp_ax.set_xlabel(r"T$_{TA98}$"+u" (ºC)")
    comp_ax.set_ylabel(r"T$_{REE}$"+u" (ºC)")
    comp_ax.yaxis.set_ticks([950,1000,1050,1100])
    labels = comp_ax.get_yticklabels()+ax.get_yticklabels()
    for label in labels:
        label.set_rotation('vertical')

    ax.set_ylabel(u"Equilibrium T (ºC)")

    comp_ax.set_xlim(cxlim)
    comp_ax.autoscale(False)
    a = [0,2000]
    comp_ax.plot(a,a, c="#cccccc", zorder=-20)

    sns.despine(ax=ax)
    sns.despine(ax=comp_ax, left=True, right=False, top=True)
    sns.despine(ax=ax1,left=True,bottom=True, right=False)

    axis_labels(ax,ax1, fontsize=16, pad=0.12)

    fig.savefig("build/pyx-dree.pdf",bbox_inches="tight", dpi=300)
