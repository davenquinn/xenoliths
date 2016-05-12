import numpy as N
import matplotlib.pyplot as P
from pandas import read_sql
from paper import plot_style
from paper.query import sample_colors
from matplotlib.ticker import ScalarFormatter
from xenoliths.application import app, db
from xenoliths.SIMS.query import sims_data, element_data, ree_only
from xenoliths.core.models import Sample

with app.app_context():

    data = ree_only(sims_data())
    colors = sample_colors()

all_cols = data.reset_index()
ticks = all_cols['element'].unique()
symbols = all_cols['symbol'].unique()
plot_data = element_data(data).join(colors)

fig, ax = P.subplots(1,1,figsize=(5,5))

minerals = ('cpx','opx')
labels = ('cpx',
          'opx',
          'Whole rock')

for mineral in minerals:
    _ = lambda x: x[1] == mineral
    min_data = plot_data[plot_data.index.map(_)]
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

    ax.set_yscale('log')
    ax.set_xlim([ticks[0]-0.5,ticks[-1]+0.5])

    kw = dict(color='#888888',fontsize=10)
    ax.text(x[0],20,"Clinopyroxene",**kw)
    ax.text(x[0],.3,"Orthopyroxene",**kw)

    ax.yaxis.set_ticklabels(["{:g}".format(v) for v in ax.yaxis.get_ticklocs()])
    ax.set_ylabel("Pyroxene REE / CI chondrite")

ax.xaxis.set_ticks(ticks)
ax.xaxis.set_ticklabels(symbols)

fig.savefig("build/trace-elements.pdf", bbox_inches="tight")


