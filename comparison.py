#!/usr/bin/env python
"""
Generate a figure comparing cpx depletion trends to
those of abyssal peridotites.

Uses data from [Warren, 2016, doi:10.1016/j.lithos.2015.12.023]
"""
from __future__ import division

import numpy as N
import pandas as P
from os import path, environ
from subprocess import Popen, PIPE
from xenoliths import app, db
from xenoliths.models import Sample

import matplotlib.pyplot as plt
from paper.query import sample_colors
from paper import plot_style
from periodictable import elements
from xenoliths.SIMS.query import sims_data, element_data, ree_only
from sys import argv

from shared import mineral_data

with app.app_context():
    data = ree_only(sims_data())
    colors = sample_colors()
    all_cols = data.reset_index()
    plot_data = element_data(data).join(colors)
    min_data = mineral_data(plot_data,'cpx')

all_cols = data.reset_index()
ticks = all_cols['element'].unique()
symbols = all_cols['symbol'].unique()

# Get literature modal mineralogy data
data_dir = environ.get('DATA_DIR')
fn = path.join(data_dir,'literature','Warren (2016) abyssal peridotites','mmc1-2.xls')
df = P.read_excel(fn, index_col=0, skiprows=[0])

chondrite = P.read_csv('chondrite.csv',comment='#',index_col=0)
df = df[(df.Lithology == 'Lherz')]
trace_el = df.iloc[:,49:62]
# Filter data with no trace elements
trace_el = trace_el[trace_el.sum(axis=1).notnull()]

fig, ax = plt.subplots(1,1,figsize=(5,5))

cols = list(trace_el.columns)
norm = 1000/N.array(chondrite.T)[0]
ixs = N.array([getattr(elements,i).number for i in cols])
for ix,row in trace_el.iterrows():
    d = N.array(row)*norm[:-1]
    msk = ~N.isnan(d)
    ax.plot(ixs[msk],d[msk], color='#dddddd', linewidth=2)

# Plot Crystal Knob data
for ix,row in min_data.iterrows():
    color = row.pop('color')
    n = row.pop('n')

    x = list(row.index)
    u = N.array([m.n for m in row])
    s = N.array([m.s for m in row])

    # Dirty hack to prevent weird error artifacts
    s[s > u] /= 2
    # Should maybe implement proper log errors
    # (i.e. not asymmetric

    ax.fill_between(x,u-s,u+s,
        facecolor=color,
        edgecolor='none',
        alpha=0.2)
    ax.plot(x,u, color=color)

ticks = all_cols['element'].unique()
symbols = all_cols['symbol'].unique()

ax.set_yscale('log')
ax.set_xlim([ticks[0]-0.5,ticks[-1]+0.5])

kw = dict(color='#888888',fontsize=10)
ax.yaxis.set_ticklabels(["{:g}".format(v) for v in ax.yaxis.get_ticklocs()])
ax.set_ylabel("Clinopyroxene REE / CI chondrite")

ax.xaxis.set_ticks(ticks)
ax.xaxis.set_ticklabels(symbols)

fig.savefig(argv[1], bbox_inches="tight")

