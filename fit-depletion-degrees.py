from __future__ import division

from sys import argv
from xenoliths import app
from xenoliths.SIMS.query import sims_data, element_data
from depletion_model import get_tables, get_melts_data
from periodictable import elements
from IPython import embed

def process_data():
    df = sims_data(ree_only=True, raw=True, whole_rock=True)
    df = element_data(df)
    val = df.index.get_level_values('mineral')=='whole_rock'
    df = df.loc[val]
    df.index = df.index.droplevel(1)
    df.drop('n', axis=1, inplace=True)
    df.columns = [elements[i].symbol for i in df.columns]
    return df

with app.app_context():
    data = process_data()

# Create primitive-mantle normalized dataset
Sun_PM = get_melts_data('literature/Sun_McDonough_PM.melts')
PM_trace = Sun_PM.trace.ix[:,0]
data /= PM_trace
data.dropna(axis=1,how='all',inplace=True)

depletion = get_tables(argv[1])
embed()
