from __future__ import division

from sys import argv
from xenoliths import app
from xenoliths.SIMS.query import sims_data, element_data
from depletion_model import get_tables
from IPython import embed

def process_data():
    df = sims_data(ree_only=True, raw=True, whole_rock=True)
    df = element_data(df)
    val = df.index.get_level_values('mineral')=='whole_rock'
    df = df.loc[val]
    df.index = df.index.droplevel(1)
    return df

with app.app_context():
    data = process_data()

depletion = get_tables(argv[1])

embed()
