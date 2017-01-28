#!/usr/bin/env python
# -- coding: utf-8 --
from __future__ import print_function

import json
import numpy as N
import sys
from collections import defaultdict

from xenoliths import app, db
from xenoliths.thermometry.pressure import pressure_measurements, geobaric_gradient
from paper.query import xenolith_minerals
from scipy.stats import norm, gaussian_kde
from max_stability import max_depth
from pickle import load

datafile = sys.argv[1]
outfile = sys.argv[2]
with open(datafile) as f:
    data = load(f)

q = "SELECT dz, heat_flow, temperature FROM thermal_modeling.static_profile"

with app.app_context():
    spinel_cr = {k['id']: k['sp']['cr_number'].n
            for k in xenolith_minerals('molar')}
    profiles = db.session.execute(q).fetchall()

for res in data:
    depth = res['depth']
    c = res['sample_color']
    T = res['temperature']
    ax.plot(T,depth)
    # Maximum depth based on spinel Cr content
    id = res['sample_id']
    T = N.sort(res['temperature'][::100])
    d = max_depth(T,spinel_cr[id]/100)
    dz = 0.15/0.03 # GPa / # G
    # Plot maximum stability
    ax.fill_between(T,d+dz,d-dz)
    # 0.15 GPa error bars assumed

# Plot Plagioclase in
# rough, from Green and Ringwood,1970
x,y = [700,1200],[21,27]
ax.plot(x,y)

# Heat flow
cells = N.arange(len(T))*dz+dz/2
Z = cells/1000

lwx=1
if heat_flow == 90:
    lwx = 2
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

