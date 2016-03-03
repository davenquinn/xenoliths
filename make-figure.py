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

outfile = sys.argv[1]
with app.app_context():
    data = pressure_measurements(uncertainties=False,core=True, n=10)

    spinel_cr = {k['id']: k['sp']['cr_number'].n
            for k in xenolith_minerals('molar')}

    fig, ax = subplots(figsize=(4,4))
    for sample,res in data:
        #ax.scatter(t["T_ta98"], t["heatflow"]["z"], marker="o", s=10, alpha=0.4, color="#cccccc", zorder=-10)
        temps = N.array([t.temperature for t in res])
        ax.scatter(
            temps,
            [t.depth for t in res],
            marker="o",
            s=20,
            alpha=0.3,
            color=sample.color)

        # Maximum depth based on spinel Cr content
        d = max_depth(temps,spinel_cr[sample.id]/100)
        ax.scatter(
            temps,
            d,
            marker=".",
            s=35,
            color=sample.color)

ax.invert_yaxis()
ax.set_xlabel(u"Temperature - TA98 (\u00b0C)")
ax.set_ylabel(u"Depth (km)")
#ax.set_xlim([940,1150])
#ax.set_xlim([950,1150])
#ax.set_ylim([110,50])
ax.set_ylim([110,50])
#ax.autoscale(False)
# y = N.linspace(0,150,150)
# m = HeatFlowModel(q_0=:90)
# T = N.array(map(m.temperature, y))
# ax.plot(T,y,color="#cccccc", zorder=-20)

fig.savefig(outfile, bbox_inches="tight")
