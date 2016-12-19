#!/usr/bin/env python

from xenoliths import app
import matplotlib.pyplot as P
from sys import argv
from paper import plot_style
from query import spinel_data
from xenoliths.microprobe.spinel import correct_spinel

with app.app_context():
    spinels = spinel_data()
    colors = [s.sample.color for s in spinels]
    data = [correct_spinel(s, uncertainties=False) for s in spinels]

    cr_number = [c['Cr']/(c['Cr']+c['Al'])*100 for c in data]
    mg_number = [c['Mg']/(c['Mg']+c['Fe'])*100 for c in data]

    fig, ax = P.subplots(figsize=(4,4))
    ax.scatter(mg_number,cr_number,
            c=colors, edgecolor=colors)
    ax.set_ylabel('Cr#')
    ax.set_xlabel('Mg#')

    fig.savefig(argv[1], bbox_inches='tight')

