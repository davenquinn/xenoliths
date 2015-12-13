from pandas import DataFrame, concat

from paper.query import xenolith_minerals
from xenoliths.application import app, db
from xenoliths.models import Sample
from xenoliths.SIMS.query import sims_data as base_data

def element_data(data,columns='element'):
    all_cols = data.reset_index()

    ix = ['sample_id','mineral']
    n = all_cols.groupby(ix)['n'].max()
    df = all_cols.pivot_table(
            rows=ix,
            columns=columns,
            values=['average'],
            aggfunc=lambda x: x)
    df.columns = df.columns.get_level_values(1)
    return df.join(n)

def sims_data(whole_rock=False, **kwargs):
    data = base_data(**kwargs)
    if not whole_rock:
        return data

    xenoliths = (db.session.query(Sample)
        .filter_by(xenolith=True))
    modes = {s.id:s.modes() for s in xenoliths.all()}
    df = DataFrame.from_dict(modes, orient='index')
    df = df.stack()
    df.name = 'mode'
    ix = ['sample_id','mineral']
    df.index.names = ix

    d1 = data.reset_index().join(df,on=ix)
    d1['average'] = d1['mode']*d1['average']
    d1 = d1.groupby(['sample_id','element','symbol'])
    d1 = d1.aggregate(dict(average=sum))
    d1['mineral'] = 'whole_rock'
    d1.set_index('mineral',append=True, inplace=True)
    d1 = d1.reorder_levels(data.index.names)

    return concat([data,d1])
