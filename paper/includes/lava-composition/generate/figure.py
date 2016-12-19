"""
Generate a total-alkali vs. silica plot
for the lava.
"""
from __future__ import division
from os import path

import numpy as N
from matplotlib import pyplot as P
import tasplot

from xenoliths.microprobe.group import get_oxides
from .query import queryset

def make_tas():
    here = path.dirname(__file__)

    ox=[get_oxides(d)
            for d in queryset.all()]

    # Normalize to 100%
    totals = N.array([sum(o.values()) for o in ox])

    ta = N.array([d['K2O']+d['Na2O'] for d in ox])
    s = N.array([d['SiO2'] for d in ox])

    ta_n = ta * 100/totals
    s_n = s * 100/totals

    fig,ax = P.subplots()
    tasplot.add_LeMaitre_fields(ax)

    #ax.plot(s,ta, 'r.', label='Raw data')
    ax.plot(s_n,ta_n, '.', label='Normalized to 100%')

    #ax.legend()

    fig.savefig('build/tas.pdf', bbox_inches='tight')
