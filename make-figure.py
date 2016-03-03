#!/usr/bin/env python
# -- coding: utf-8 --

import json
import numpy as N
import sys
from chroma import Color
from matplotlib.pyplot import subplots
from collections import defaultdict

from xenoliths import app
from xenoliths.thermometry.pressure import pressure_measurements
from paper.query import xenolith_minerals
from max_stability import max_depth
from pickle import load

datafile = sys.argv[1]
outfile = sys.argv[2]
with open(datafile) as f:
    data = load(f)

with app.app_context():
    spinel_cr = {k['id']: k['sp']['cr_number'].n
            for k in xenolith_minerals('molar')}

fig, ax = subplots(figsize=(4,4))
for res in data:
    #ax.scatter(t["T_ta98"], t["heatflow"]["z"], marker="o", s=10, alpha=0.4, color="#cccccc", zorder=-10)
    T = res['temperature']
    ax.scatter(
        T,
        res['depth'],
        marker="o",
        s=20,
        alpha=0.3,
        color=res['sample_color'])

    # Maximum depth based on spinel Cr content
    id = res['sample_id']
    d = max_depth(T,spinel_cr[id]/100)
    ax.scatter(
        T,d,
        marker=".",
        s=35,
        color=res['sample_color'])

ax.invert_yaxis()
ax.set_xlabel(u"Temperature - TA98 (\u00b0C)")
ax.set_ylabel(u"Depth (km)")
ax.set_ylim([110,40])
#ax.autoscale(False)
# y = N.linspace(0,150,150)
# m = HeatFlowModel(q_0=:90)
# T = N.array(map(m.temperature, y))
# ax.plot(T,y,color="#cccccc", zorder=-20)

fig.savefig(outfile, bbox_inches="tight")
