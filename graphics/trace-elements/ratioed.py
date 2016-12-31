import numpy as N
import matplotlib.pyplot as P
from pandas import read_sql
from paper.query import sample_colors
from paper import plot_style
from xenoliths.application import app, db
from xenoliths.SIMS.query import sims_data, element_data, ree_only
from xenoliths.core.models import Sample
from sys import argv

from shared import mineral_data

with app.app_context():
    data = ree_only(sims_data())
    colors = sample_colors()

fig, ax = P.subplots(figsize=(5,4))

all_cols = data.reset_index()
ticks = all_cols['element'].unique()
symbols = all_cols['symbol'].unique()

opx = mineral_data(data, 'opx')
data = mineral_data(data, 'cpx')
data['average'] = data['average']/opx['average']

data = element_data(data, index='sample_id').join(colors)

for ix,row in data.iterrows():
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

ax.set_yscale('log')
ax.set_xlim([ticks[0]-0.5,ticks[-1]+0.5])

ax.set_ylabel("Cpx/Opx")

ax.xaxis.set_ticks(ticks)
ax.xaxis.set_ticklabels(symbols)

fig.savefig(argv[1], bbox_inches="tight")



