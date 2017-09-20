import numpy as N
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as P
from pandas import read_sql, read_excel, read_csv
from paper.plot_style import update_axes, axis_labels
from paper.query import sample_colors
from matplotlib.ticker import ScalarFormatter
from xenoliths.application import app, db
from xenoliths.SIMS.query import sims_data, element_data
from xenoliths.core.models import Sample
from os import environ, path

from enrichment_trends import enrichment_trends
from shared import mineral_data

with app.app_context():

    data = sims_data(ree_only=True)
    colors = sample_colors()

all_cols = data.reset_index()
ticks = all_cols['element'].unique()
symbols = all_cols['symbol'].unique()
plot_data = element_data(data).join(colors)

fig, (ax, ax2) = P.subplots(2,1,
    figsize=(3.75,7),
    gridspec_kw=dict(
        height_ratios=(3.2,2)))

minerals = ('cpx','opx')
labels = ('cpx',
          'opx',
          'Whole rock')

for mineral in minerals:
    min_data = mineral_data(plot_data,mineral)
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
    ax.set_xlim([ticks[0]-0.1,ticks[-1]])

    kw = dict(color='#888888',fontsize=10)
    ax.text(x[0],20,"Clinopyroxene",**kw)
    ax.text(65,.3,"Orthopyroxene",rotation=26,**kw)

    ax.yaxis.set_ticklabels(["{:g}".format(v) for v in ax.yaxis.get_ticklocs()])
    ax.set_ylabel("Pyroxene rare-earth abundance / CI chondrite", labelpad=-1)

ax.xaxis.set_ticks(ticks)
ax.xaxis.set_ticklabels(symbols)
update_axes(ax)

#### Plot literature field

"""
Generate a figure comparing cpx depletion trends to
those of abyssal peridotites.

Uses data from [Warren, 2016, doi:10.1016/j.lithos.2015.12.023]
"""
from periodictable import elements

# Get literature modal mineralogy data
data_dir = environ.get('DATA_DIR')
fn = path.join(data_dir,'literature','Warren (2016) abyssal peridotites','mmc1-2.xls')
df = read_excel(fn, index_col=0, skiprows=[0])

chondrite = read_csv('chondrite.csv',comment='#',index_col=0)
df = df[(df.Lithology == 'Lherz')]
trace_el = df.iloc[:,49:62]

# Filter data with no trace elements
trace_el = trace_el[trace_el.sum(axis=1).notnull()]
## Filter spurious values of La
trace_el = trace_el[trace_el["La"]<2]
trace_el = trace_el[trace_el["Yb"]>2]

## Guesstimate Lu from Yb
trace_el["Lu"] = trace_el["Yb"]

# Filter weird outlier
Tb = trace_el['Tb']
trace_el = trace_el[Tb.min() != Tb]

cols = list(trace_el.columns)
norm = 1000/N.array(chondrite.T)[0]
ixs = N.array([getattr(elements,i).number for i in cols])
for ix,row in trace_el.iterrows():
    d = N.array(row)*norm[:-1]
    msk = ~N.isnan(d)
    ax.plot(ixs[msk],d[msk], color='#eeeeee', linewidth=2, zorder=-10)


#### Enrichment trends in cpx
enrichment_trends(ax2, data, colors)
update_axes(ax2)
ax2.locator_params(nbins=4, axis='y')
ax2.locator_params(nbins=5, axis='x')
fig.tight_layout()
fig.subplots_adjust(hspace=0.09, right=1, left=0.035)

kw = dict(color='#888888',fontsize=10)
ax.text(x[0],20,"Clinopyroxene",**kw)

axis_labels(ax,ax2)
fig.savefig("build/trace-elements.pdf", bbox_inches="tight")


