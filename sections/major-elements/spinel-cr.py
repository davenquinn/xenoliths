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
from colour import Color

with app.app_context():
    spinels = spinel_data()
    colors = [s.sample.color for s in spinels]

    lighter_colors = lambda lum: [Color(c, luminance=lum).hex
                                  for c in colors]

    edgecolors = list(lighten(*colors, lum=0.1))

    data = [correct_spinel(s, uncertainties=False) for s in spinels]

    # Use all tetrahedral cations in the calculation of corrected Cr#
    cr_number = [c['Cr']/(c['Cr']+c['Al'])*100 for c in data]
    mg_number = [c['Mg']/(c['Mg']+c['Fe'])*100 for c in data]

    fig, ax = P.subplots(figsize=(4,4))
    ax.scatter(mg_number,cr_number,
            c=edgecolors,
            edgecolor=colors,
            alpha=0.8,
            label='Corrected')

    ## Annotations
    # Group data
    with open("spinel-cr-annotations.yaml",'r') as f:
        annotation_data = yaml.load(f.read())

    samples = [s.sample.id for s in spinels]
    df = DataFrame(
        data=N.array([mg_number, cr_number]).T,
        index=samples)

    vals = annotation_data['default']
    for id in df.index.unique():
        sm = df.ix[df.index == id]
        pos = tuple(sm.mean())

        v_ = annotation_data.get(id,None)
        if v_ is not None:
            v_ = dict(vals,**v_)
        ax.annotate(id, xy=pos, **v_)

    __xlabel = "Mg#"
    #### Plot against uncorrected data
    if os.environ.get("PLOT_UNCORRECTED",False):
        spinel_cations = [get_cations(o, oxygen=4, uncertainties=False)
                          for o in spinels]
        cr_number = [c['Cr']/(c['Cr']+c['Al'])*100 for c in spinel_cations]
        mg_number = [c['Mg']/(c['Mg']+c['Fe'])*100 for c in spinel_cations]

        ax.scatter(mg_number, cr_number,
                   c=list(lighten(*colors, lum=0.45, sat=-0.1)),
                   marker='s',
                   edgecolor=list(lighten(*colors,lum=0.38, sat=-0.)),
                   alpha=0.8,
                   label='Uncorrected')

        ax.legend(loc='lower left')
    else:
        __xlabel += " (corrected)"

    ax.set_ylabel('Cr#')
    ax.set_xlabel(__xlabel)

    update_axes(ax)
    fig.savefig(argv[1], bbox_inches='tight')

