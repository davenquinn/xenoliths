from __future__ import division, print_function

from sys import argv
import numpy as N
from xenoliths import app
from pandas import DataFrame, read_table
from xenoliths.SIMS.query import sims_data, element_data
from depletion_model import get_melts_data, ree_plot
from depletion_model.util import element, ree_data
from depletion_model import DepletionModel
from xenoliths.core import sample_colors
from paper import plot_style

# Whole-rock or CPX fitting
mode = 'whole_rock'

def process_data():
    df = sims_data(ree_only=True, raw=True, whole_rock=True)
    df = element_data(df)
    val = df.index.get_level_values('mineral')==mode
    df = df.loc[val]
    df.index = df.index.droplevel(1)
    df.drop('n', axis=1, inplace=True)
    df.columns = [element(i) for i in df.columns]
    return df

with app.app_context():
    data = process_data()
    colors = sample_colors()

# Create primitive-mantle normalized dataset
Sun_PM = get_melts_data('literature/Sun_McDonough_PM.melts')
PM_trace = Sun_PM.trace.ix[:,0]
data /= PM_trace
data.dropna(axis=1,how='all',inplace=True)

model = DepletionModel(argv[1], log_fit=True)

# Fit HREEs
Tb, Lu = element('Tb'), element('Lu')
func = lambda i: Tb <= element(i) <= Lu
depleted = model.fit('Solid Trace', data, func)

# Get mineral-melt partition coefficients for ending conditions
# Could also just use computed values
coeffs = model.tables['Partition Coefficients']
params = [coeffs.loc[int(row['step_index'])]
            for i,row in depleted.iterrows()]
Dree = DataFrame(params).set_index(depleted.index)

# Re-enrichment model
# Currently, enrichment is modeled as a fully batch process
delta = (data-depleted)
enrichment = ree_data((data+delta)/Dree)
enrichment = enrichment.applymap(lambda x: x.nominal_value)

# Normalize to mean HREE *(in log space)
hree = N.exp(N.log(enrichment[[66,67,68,70,71]]).mean(axis=1))
# Amount of enriched liquid that is needed to reset values
bias = hree/6
enrichment = enrichment.div(bias,axis=0)

# Add NMORB
NMORB = get_melts_data('literature/NMORB_trace.melts')
NMORB_trace = ree_data(NMORB.trace.transpose()/PM_trace)

# Alkali basalt
alkali = read_table('literature/Farmer_1995-Alkali-basalt.txt',
                    comment="#", index_col=0)
alkali /= PM_trace
alkali_trace = ree_data(alkali)

vals = map(element,data.columns)
d = ree_data(depleted)
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

    ax.set_ylim(.001,100)
    ax.set_xlim(element('La')-0.3,element('Lu')+0.3)
    ax.yaxis.set_ticklabels(["{:g}".format(v) for v in ax.yaxis.get_ticklocs()])
    ax.set_ylabel("REE / Primitive Mantle")
    ax.xaxis.set_ticks(vals)
    ax.xaxis.set_ticklabels(data.columns)

# Get depletion degrees using various methods
from IPython import embed
embed()
