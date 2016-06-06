from __future__ import division, print_function

from sys import argv
import numpy as N
from xenoliths import app
from pandas import DataFrame
from xenoliths.SIMS.query import sims_data, element_data
from depletion_model import get_tables, get_melts_data
from depletion_model.util import element
from IPython import embed

def process_data():
    df = sims_data(ree_only=True, raw=True, whole_rock=True)
    df = element_data(df)
    val = df.index.get_level_values('mineral')=='whole_rock'
    df = df.loc[val]
    df.index = df.index.droplevel(1)
    df.drop('n', axis=1, inplace=True)
    df.columns = [element(i) for i in df.columns]
    return df

with app.app_context():
    data = process_data()

# Create primitive-mantle normalized dataset
Sun_PM = get_melts_data('literature/Sun_McDonough_PM.melts')
PM_trace = Sun_PM.trace.ix[:,0]
data /= PM_trace
data.dropna(axis=1,how='all',inplace=True)

depletion = get_tables(argv[1])
trace = depletion['Solid Trace']

# Fit data against trace element depletion curve

# Only use HREE
Tb, Lu = element('Tb'), element('Lu')
def drop_unused(df):
    cols = [i for i in df.columns
        if not Tb <= element(i) <= Lu
            or i == 'Tm'] #Technetium is not in anything
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
    series['sse'] = sse.loc[ix]
    series['sample'] = row.name
    return series

# Find best-fitting simulation step for each sample
serie = [__best_fit(row)
        for i,row in fit.iterrows()]
depleted = DataFrame(serie)
embed()
