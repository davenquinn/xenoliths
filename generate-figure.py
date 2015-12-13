import numpy as N
import matplotlib.pyplot as P
from pandas import read_sql
from paper.query import sample_colors
from xenoliths.application import app, db
from xenoliths.SIMS.query import sims_data, ree_only
from xenoliths.core.models import Sample

with app.app_context():

    data = ree_only(sims_data())
    colors = sample_colors()


fig, ax = P.subplots(1, figsize=(5,5))

all_cols = data.reset_index()
ticks = all_cols['element'].unique()
symbols = all_cols['symbol'].unique()

ix = ['sample_id','mineral']
n = all_cols.groupby(ix)['n'].max()
plot_data = (all_cols.pivot_table(
    rows=ix,
    columns=['element'],
    values=['average'],
    aggfunc=lambda x: x)
    .join(n)
    .join(colors))

for ix,row in plot_data.iterrows():
    color = row.pop('color')
    n = row.pop('n')

    x = N.array([i[1] for i in row.index])
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

ax.xaxis.set_ticks(ticks)
ax.xaxis.set_ticklabels(symbols)
ax.set_xlim([ticks[0]-0.5,ticks[-1]+0.5])

ax.set_ylabel("REE / CI chondrite")

fig.savefig("build/trace-elements.pdf", bbox_inches="tight")


