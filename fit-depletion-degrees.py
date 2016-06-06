from __future__ import division, print_function

from sys import argv
import numpy as N
from xenoliths import app
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
    df.drop(cols,axis=1,inplace=True)

# Prepare trace elements for fitting
# Ignore uncertainties for fitting and copy dataset
fit = data.applymap(lambda x: x.nominal_value)

iters = trace.set_index(['mass','Pressure','Temperature'])
drop_unused(iters)
drop_unused(fit)

# Linearize data for minimization
fit = N.log(fit)
iters = N.log(iters)

for i,row in fit.iterrows():
    residuals = row-iters
    sse = (residuals**2).sum(axis=1)
    ix = sse.idxmin()
    print(row.name,ix, sse[ix])

embed()
