#!/usr/bin/env python

import os
import matplotlib
matplotlib.use('Agg')
from xenoliths import app
import matplotlib.pyplot as P
import numpy as N
import yaml
from pandas import DataFrame
from sys import argv
from paper.plot_style import update_axes, lighten
from query import spinel_data
from spinel_calc import correct_spinel, get_cations
from json import dump

with app.app_context():
    spinels = spinel_data()
    data = [correct_spinel(s, uncertainties=False) for s in spinels]
    # Use all tetrahedral cations in the calculation of corrected Cr#
    cr_number = [c['Cr']/(c['Cr']+c['Al'])*100 for c in data]
    mg_number = [c['Mg']/(c['Mg']+c['Fe'])*100 for c in data]

    samples = [s.sample.id for s in spinels]
    df = DataFrame(
        data=N.array([mg_number, cr_number]).T,
        columns=["mg_number","cr_number"],
        index=samples)

    g = df.groupby(df.index)

    mn = g.mean()
    std = g.std().rename(columns=lambda s: s+"_std")
    df = mn.join(std)

    with open(argv[1],'w') as f:
        f.write(df.to_json(orient='index'))

