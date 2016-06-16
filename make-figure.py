#!/usr/bin/env python
# -- coding: utf-8 --

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
from max_stability import max_depth
from pickle import load
from chroma import Color

datafile = sys.argv[1]
outfile = sys.argv[2]
with open(datafile) as f:
    data = load(f)

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
        alpha=0.05,
        linewidth=0)
    ax.plot(
        T,d,
        color=c)
    for s in (1,-1):
        ax.plot(T,d+s*dz,':',color=c,linewidth=1,dashes=(1,2),alpha=0.8)

    kernel = gaussian_kde(depth, 0.1)
    Z = N.linspace(depth.min()-10,depth.max()+10,200)
    v = kernel(Z)
    ax1.fill_betweenx(Z,0,v,facecolor=c, alpha=0.05)
    ax1.plot(v,Z,color=c, alpha=0.5, linewidth=1.5)

    ax1.annotate("Ca-in-olivine", xy=(.5,.35),
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
ax.plot(x,y,':',color="#aaaaaa")
kws = dict(
    xy=(1100,26),
    color='#aaaaaa',
    rotation=-4,
    ha='center',
    size=8)
ax.annotate('Plagioclase',va='bottom',**kws)
ax.annotate('Spinel',va='top',**kws)

kws.update(rotation=-8,xy=(950,85))
ax.annotate('Garnet',**kws)

ax.autoscale(False)
c = "#cccccc"
for dz, heat_flow, T in profiles:
    cells = N.arange(len(T))*dz+dz/2
    Z = cells/1000
    ax.plot(T,Z,color=c, zorder=-20)
    for i,v in enumerate(T):
        if v > 1120: break
    d = Z[i]

    a = N.arctan2(-d+Z[i-1],v-T[i-1])
    ax.text(v,d-0.9,"{0} ".format(heat_flow)+r"$mW/m^2$",rotation=5.5*N.degrees(a),
            va='center',ha='center',color='#aaaaaa',size=7)

fig.savefig(outfile, bbox_inches="tight", dpi=300)
