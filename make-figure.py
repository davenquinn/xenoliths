#!/usr/bin/env python
# -- coding: utf-8 --

import json
import numpy as N
import sys
from chroma import Color
from matplotlib.pyplot import subplots, style
from collections import defaultdict
from paper import plot_style

from xenoliths import app, db
from xenoliths.thermometry.pressure import pressure_measurements, geobaric_gradient
from paper.query import xenolith_minerals
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

fig, ax = subplots(figsize=(4,4))
for res in data:
    T = res['temperature']
    ax.plot(
        T,
        res['depth'],
        ".",
        alpha=0.5,
        color=res['sample_color'])

    # Maximum depth based on spinel Cr content
    id = res['sample_id']
    d = max_depth(T,spinel_cr[id]/100)
    dz = 0.15/0.03 # GPa / # G
    ax.fill_between(
        T,d+dz,d-dz,
        color=res['sample_color'],
        alpha=0.2)
    ax.plot(
        T,d,
        color=res['sample_color'])

ax.invert_yaxis()
ax.set_xlabel(u"Temperature - TA98 (\u00b0C)")
ax.set_ylabel(u"Depth (km)")
ax.set_ylim([90,30])

ax.autoscale(False)
for dz, profile, T in profiles:
    assert T[0] != 0
    cells = N.arange(len(T))*dz+dz/2
    ax.plot(T,cells/1000,color="#cccccc", zorder=-20)

fig.savefig(outfile, bbox_inches="tight")
