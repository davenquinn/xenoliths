#!/usr/bin/env python
# -- coding: utf-8 --
from __future__ import print_function

import json
import numpy as N
import matplotlib as M
import sys
from seaborn.apionly import despine
from chroma import Color
from matplotlib.pyplot import figure, style
from collections import defaultdict
from paper import plot_style

from xenoliths import app, db
from xenoliths.thermometry.pressure import pressure_measurements, geobaric_gradient
from paper.query import xenolith_minerals
from scipy.stats import norm, gaussian_kde
from thermodynamics import max_depth
from statistics import barometer_kernel_density, load_data
from matplotlib.patches import Polygon
from chroma import Color

datafile = sys.argv[1]
outfile = sys.argv[2]
data = load_data(datafile)

q = "SELECT dz, heat_flow, temperature FROM thermal_modeling.static_profile"

with app.app_context():
    spinel_cr = {k['id']: k['sp']['cr_number'].n
            for k in xenolith_minerals('molar')}
    profiles = db.session.execute(q).fetchall()

fig = figure(figsize=(4,5.5), dpi=300)

gs = M.gridspec.GridSpec(1, 2, width_ratios=[4,1], wspace=0)

ax = fig.add_subplot(gs[0])
ax1 = fig.add_subplot(gs[1], sharey=ax)

for res in data:
    depth = res['depth']
    c = res['sample_color']
    T = res['temperature']
    ax.plot(
        T,
        depth,
        ".",
        alpha=0.01,
        color=c,
        rasterized=True)

    # Maximum depth based on spinel Cr content
    id = res['sample_id']
    T = N.sort(res['temperature'][::100])
    d = max_depth(T,spinel_cr[id]/100)
    dz = 0.15/0.03 # GPa / # G
    ax.fill_between(
        T,d+dz,d-dz,
        color=c,
        alpha=0.1,
        linewidth=0)
    ax.plot(
        T,d,':',
        color=c,
        linewidth=1.5,
        dashes=(3,1),alpha=0.8)
    for s in (1,-1):
        ax.plot(T,d+s*dz,color=c,linewidth=0.4,alpha=0.5)

    kernel = barometer_kernel_density(depth)
    Z = N.linspace(depth.min()-10,depth.max()+10,200)
    v = kernel(Z)
    ax1.fill_betweenx(Z,0,v,facecolor=c, alpha=0.05)
    ax1.plot(v,Z,color=c, alpha=0.5, linewidth=1.5)

loc = (.6,.30)
ax1.annotate(r"Ca-in-olivine", xy=loc,
    weight='bold',
    xycoords='axes fraction',rotation=-90,color='#aaaaaa',size=10)
ax1.annotate(r"kernel density", xy=loc,
    textcoords='offset points', xytext=(-10,0),
    style='italic',
    xycoords='axes fraction',rotation=-90,color='#aaaaaa',size=10)


ax.invert_yaxis()
ax.set_xlabel(u"Temperature - TA98 (\u00b0C)")
ax.set_ylabel(u"Depth (km)")
ax.set_ylim([90,10])
ax.set_xlim([900,1150])

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
despine(ax=ax1,left=False,bottom=True, right=True)
ax1.yaxis.set_ticks_position('none')
ax1.xaxis.set_ticks([])
for label in ax1.get_yticklabels():
    label.set_visible(False)
# Plot Plagioclase in
# rough, from Green and Ringwood,1970
x,y = [700,1200],[21,27]
ax.plot(x,y,':',color="#aaaaaa", dashes=(2,1), linewidth=1.5)
kws = dict(
    xy=(1100,26),
    color='#aaaaaa',
    rotation=-4,
    ha='center',
    weight='bold',
    style='italic',
    size=8)
ax.annotate('Plagioclase',va='bottom',**kws)
ax.annotate('Spinel',va='top',**kws)

kws.update(rotation=-8,xy=(950,85))
ax.annotate('Garnet',**kws)

ax.autoscale(False)
c = "#eeeeee"
plot_area = []
for dz, heat_flow, T in profiles:
    cells = N.arange(len(T))*dz+dz/2
    Z = cells/1000

    lwx=1
    if heat_flow in [80,90]:
        lwx = 2

    if heat_flow == 80:
        plot_area += zip(T,Z)
    elif heat_flow == 90:
        plot_area += zip(T,Z)[::-1]

    ax.plot(T,Z,color=c, zorder=-20, linewidth=0.75*lwx)
    for i,v in enumerate(T):
        if v > 1145: break
    d = Z[i]

    #+r"$mW/m^2$"
    a = N.arctan2(-d+Z[i-1],v-T[i-1])
    r = 5.5*N.degrees(a)
    kwargs=dict(
        rotation=r,
        size=7,
        bbox=dict(pad=1,color='#ffffff'),
        va='center',ha='right',
        color='#bbbbbb')

    ax.text(v,d-0.1,heat_flow,
            **kwargs)
    if heat_flow == 120:
        ax.text(v,d-3.5,r"$q_0$ ($mW/m^2$)",
                style='italic',
                **kwargs)

        kw = dict(closed=True, facecolor='none', zorder=10, linewidth=0.25, linestyle=':')
xy = [(x,y) for x,y in plot_area if 950 < x < 1070]
poly = Polygon(xy, edgecolor='#444444', **kw)
ax.add_patch(poly)

fig.savefig(outfile, bbox_inches="tight", dpi=300)
