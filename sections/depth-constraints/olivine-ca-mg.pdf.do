#!/usr/bin/env python
from __future__ import division, print_function
import matplotlib
matplotlib.use('Agg')
from xenoliths import app
from xenoliths.thermometry import pressure
import matplotlib.pyplot as P
import numpy as N
import sys
from sys import argv
from paper.plot_style import update_axes, lighten
from subprocess import call

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
sys.stdout = sys.stderr
call(["redo-ifchange",pressure.__file__])

with app.app_context():
    olivines = pressure.pressure_olivines()
    colors = [s.sample.color for s in olivines]

    edgecolors = list(lighten(*colors, lum=0.1))

    formulae = [pressure.get_cations(ol, oxygen=4, uncertainties=False)
        for ol in olivines]

    mg = [f['Mg']/7*100 for f in formulae]
    ca = [f['Ca']/7*1e6 for f in formulae]

    fig, ax = P.subplots(figsize=(4,4))
    ax.scatter(mg,ca,
            c=edgecolors,
            edgecolor=colors,
            alpha=0.8,
            label='Corrected')

    ax.set_ylabel('Ca (ppm)')
    ax.set_xlabel('Mg (%)')

    update_axes(ax)
    fig.savefig(argv[3], bbox_inches='tight', format='pdf')


