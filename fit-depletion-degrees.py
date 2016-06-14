from __future__ import division, print_function

from sys import argv
import numpy as N
from xenoliths import app
from pandas import DataFrame
from xenoliths.SIMS.query import sims_data, element_data
from depletion_model import get_tables, get_melts_data, ree_plot
from depletion_model.util import element, ree_data
from xenoliths.core import sample_colors
from IPython import embed

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

depletion = get_tables(argv[1])
v = 'Solid Trace' if mode=='whole_rock' else 'clinopyroxene_0 trace'
trace = depletion[v]

# Fit data against trace element depletion curve

# Only use HREE
Tb, Lu = element('Tb'), element('Lu')
def drop_unused(df):
    cols = [i for i in df.columns
        if not Tb <= element(i) <= Lu]
         #   or i == 'Tm'] #Technetium is not in anything
    return df.drop(cols,axis=1)

# Prepare trace elements for fitting

iters = trace.drop(
    ['mass','Pressure','Temperature'], axis=1)
iters = drop_unused(iters)
fit = drop_unused(data)

# Ignore uncertainties for fitting
fit = fit.applymap(lambda x: x.nominal_value)

# Linearize data for minimization
fit = N.log(fit)
iters = N.log(iters)

def __best_fit(row):
    residuals = row-iters
    sse = (residuals**2).sum(axis=1)
    ix = sse.idxmin()

    series = trace.loc[ix]
    series['step_index'] = ix
    series['sse'] = sse.loc[ix]
    series['sample_id'] = row.name
    return series

# Find best-fitting simulation step for each sample
serie = [__best_fit(row)
        for i,row in fit.iterrows()]
depleted = DataFrame(serie).set_index('sample_id')

# Get mineral-melt partition coefficients for ending conditions
# Could also just use computed values
coeffs = depletion['Partition Coefficients']
params = [coeffs.loc[int(row['step_index'])]
            for i,row in depleted.iterrows()]
Dree = DataFrame(params).set_index(depleted.index)

# Get difference
delta = (data-depleted)
enrichment = ree_data((data+delta)/Dree)
enrichment = enrichment.applymap(lambda x: x.nominal_value)
enrichment.sort(axis=1,inplace=True)

# Add NMORB
NMORB = get_melts_data('literature/NMORB_trace.melts')
NMORB_trace = ree_data(NMORB.trace.transpose()/PM_trace)

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
            color='#666666', linewidth=1.5, zorder=-5)

    ax.xaxis.set_ticks(vals)
    ax.xaxis.set_ticklabels(data.columns)

# Project results back into clinopyroxene space

embed()
