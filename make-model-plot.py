from __future__ import division, print_function

from sys import argv
import numpy as N
from xenoliths import app
from pandas import DataFrame, read_table, concat
from depletion_model import get_melts_data, ree_plot, sample_ree
from depletion_model.util import element, ree_only
from depletion_model import DepletionModel
from xenoliths.core import sample_colors
from paper import plot_style
from matplotlib import pyplot as plt

with app.app_context():
    data = sample_ree(normalized=True)
    colors = sample_colors()

# Create primitive-mantle normalized dataset
Sun_PM = get_melts_data('literature/Sun_McDonough_PM.melts')
PM_trace = Sun_PM.trace.ix[:,0]

model = DepletionModel(argv[1])
depleted = model.fit_HREE(data)

# Get mineral-melt partition coefficients for ending conditions
# Could also just use computed values
coeffs = model.tables['Partition Coefficients']
params = [coeffs.loc[int(row['step_index'])]
            for i,row in depleted.iterrows()]
Dree = DataFrame(params).set_index(depleted.index)

# Re-enrichment model
# Currently, enrichment is modeled as a fully batch process
delta = (data-depleted)
# Don't know if I should divide by DREE
enrichment = ree_only((data+delta)/Dree)
enrichment = enrichment.applymap(lambda x: x.nominal_value)

# Normalize to mean HREE *(in log space)
hree = N.exp(N.log(enrichment[[66,67,68,70,71]]).mean(axis=1))
# Amount of enriched liquid that is needed to reset values
bias = 6/hree
enrichment = enrichment.mul(bias,axis=0)

# Add NMORB
NMORB = get_melts_data('literature/NMORB_trace.melts')
NMORB_trace = ree_only(NMORB.trace.transpose()/PM_trace)

# Alkali basalt
alkali = read_table('literature/Farmer_1995-Alkali-basalt.txt',
                    comment="#", index_col=0)
alkali /= PM_trace
alkali_trace = ree_only(alkali)

vals = map(element,data.columns)
d = ree_only(depleted)
with ree_plot(argv[2]) as ax:
    for i,row in d.iterrows():
        c = colors.ix[row.name][0]

        # Plot real data
        series = data.ix[row.name]
        u = series.map(lambda x: x.n)
        s = series.map(lambda x: x.s)
        ax.fill_between(vals,u-s,u+s,
            facecolor=c,
            edgecolor='none',
            alpha=0.2)
        ax.plot(vals,u, color=c)

        # Plot calculated best fit
        ax.plot(d.columns,row, color=c, linestyle='--')

        v = enrichment.ix[row.name]
        ax.plot(d.columns,v, color=c, linewidth=0.5)

    # Plot NMORB
    ax.plot(NMORB_trace.columns, NMORB_trace.ix[0,:],
            color='#888888', linewidth=1.5, zorder=-5)

    ax.fill_between(
        alkali_trace.columns,
        alkali_trace.min(),
        alkali_trace.max(),
        facecolor='#dddddd',
        edgecolor='none',
        zorder=-10)

    ax.set_ylim(.01,100)
    ax.set_xlim(element('La')-0.3,element('Lu')+0.3)
    ax.yaxis.set_ticklabels(["{:g}".format(v) for v in ax.yaxis.get_ticklocs()])
    ax.set_ylabel("REE / Primitive Mantle")
    ax.xaxis.set_ticks(vals)
    ax.xaxis.set_ticklabels(data.columns)

s = 100-depleted.mass
s.name = 'Depletion'
bias.name = 'Enrichment'
df = concat([s,bias,colors],axis=1)
fig, ax = plt.subplots(figsize=(4.25,3.75))
ax.scatter(df.Depletion,df.Enrichment,color=df.color,s=20)
for i,row in df.iterrows():
    ax.annotate(i,xy=(row.Depletion,row.Enrichment),
        color=row.color,xytext=(5,0),textcoords='offset points')
ax.set_xlabel(r'HREE depletion degrees (%)')
ax.set_ylabel(r'Proxy for re-enrichment')

fig.savefig('output/ree-trends.pdf',bbox_inches='tight')
