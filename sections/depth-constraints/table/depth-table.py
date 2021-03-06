#!/usr/bin/env python
# -- coding: utf-8 --
from __future__ import print_function
import sys
sys.path.insert(0, '..')

import json
import numpy as N
import sys
from collections import defaultdict

from xenoliths import app, db
from xenoliths.thermometry.pressure import pressure_measurements, geobaric_gradient
from paper.query import xenolith_minerals

from thermodynamics import max_depth
from statistics import barometer_kernel_density, load_data

outfile = sys.argv[2]

sample_temperatures = load_data(sys.argv[1])

q = "SELECT dz, heat_flow, temperature FROM thermal_modeling.static_profile"

with app.app_context():
    spinel_cr = {k['id']: k['sp']['cr_number'].n
            for k in xenolith_minerals('molar')}
    profiles = db.session.execute(q).fetchall()

for res in sample_temperatures:
    depth = res['depth']
    c = res['sample_color']
    T = res['temperature']
    # Maximum depth based on spinel Cr content
    id = res['sample_id']
    T = N.sort(res['temperature'][::100])
    d = max_depth(T,spinel_cr[id]/100)
    dz = 0.15/0.03 # GPa / # G
    # Plot maximum stability
    # 0.15 GPa error bars assumed

# Plot Plagioclase in
# rough, from Green and Ringwood,1970
x,y = [700,1200],[21,27]

# Heat flow
cells = N.arange(len(T))*dz+dz/2
Z = cells/1000

lwx=1

for i,v in enumerate(T):
    if v > 1145: break
d = Z[i]

#+r"$mW/m^2$"
a = N.arctan2(-d+Z[i-1],v-T[i-1])
r = 5.5*N.degrees(a)

import IPython; IPython.embed()
