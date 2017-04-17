import numpy as N
from pandas import read_sql, MultiIndex, DataFrame, concat
from sqlalchemy import func
from periodictable import La,Lu,Hf,elements

from ..application import db
from ..util import uval
from ..core.models import Sample
from .models import SIMSMeasurement as meas
from .models import SIMSDatum as datum

def sims_data(**kwargs):
    """
    Gets trace element data grouped by sample and
    minerals. The data is formatted as a nested ordered
    dictionary, for iterability. This data can be used
    as-is or averaged, as appropriate.

    kwargs:
      exclude_bad: Exclude bad items (True)
      whole_rock: Return recalculated whole-rock data (False)
      raw: Return raw data not normalized to CI chondrite (False)
      ree_only: Return only rare-earth element data (False)
    """

    exclude_bad = kwargs.pop('exclude_bad',True)
    whole_rock = kwargs.pop('whole_rock',False)
    raw = kwargs.pop('raw',False)

    if exclude_bad:
        bad_data = datum.bad.isnot(True)
    else:
        # A meaningless filter
        bad_data = True

    if raw:
        ppm, std = (datum.raw_ppm, datum.raw_std)
    else:
        ppm, std = (datum.norm_ppm, datum.norm_std)

    q = (db.session.query(datum)
        .filter(datum.element != 14)
        .filter(bad_data)
        .join(meas)
        .group_by(
            meas.sample_id,
            meas.mineral,
            datum.element)
        .with_entities(
            meas.sample_id,
            meas.mineral,
            datum.element,
            func.array_agg(ppm)
                .label('ppm'),
            func.array_agg(std)
                .label('std'),
            func.count(ppm)
                .label('n')))

    df = read_sql(q.statement,q.session.bind)

    # Apply uncertainty
    def uncertainty(row):
        vals = tuple(zip(row['ppm'],row['std']))
        return tuple(uval(n,s) for n,s in vals)

    df['norm'] = df.apply(uncertainty,axis=1)
    df = (df
        .drop('ppm', axis=1)
        .drop('std', axis=1))

    fn = lambda x: elements[x['element']].symbol
    df['symbol'] = df.apply(fn, axis=1)
    df['average'] = df['norm'].apply(N.mean)

    names = ('sample_id','mineral','element','symbol')
    df.index = MultiIndex.from_arrays(
        [df.pop(i) for i in names])
    df.sortlevel(inplace=True)

    if kwargs.pop('ree_only',True):
        df = ree_only(df)

    # Add recalculated whole-rock data if requested
    if not whole_rock:
        return df

    xenoliths = (db.session.query(Sample)
        .filter_by(xenolith=True))
    modes = {s.id:s.modes() for s in xenoliths.all()}
    modes = DataFrame.from_dict(modes, orient='index')
    modes = modes.stack()
    modes.name = 'mode'
    ix = ['sample_id','mineral']
    modes.index.names = ix

    d1 = df.reset_index().join(modes,on=ix)
    d1['average'] *= d1.pop('mode')
    d1 = d1.groupby(['sample_id','element','symbol'])
    d1 = d1.aggregate(dict(average=sum))
    d1['mineral'] = 'whole_rock'
    d1.set_index('mineral',append=True, inplace=True)
    d1 = d1.reorder_levels(df.index.names)
    return concat([df,d1])

def ree_only(df):
    ix = df.index.names.index('element')
    is_ree = lambda n: La.number <= n[ix] <= Lu.number
    return df[df.index.map(is_ree)]

def element_data(data,columns='element', index=None):
    """
    Pivots data to return a table of elements by
    mineral type and sample.
    """
    all_cols = data.reset_index()

    if not index:
        index = ['sample_id','mineral']
    n = all_cols.groupby(index)['n'].max()
    df = all_cols.pivot_table(
            index=index,
            columns=columns,
            values=['average'],
            aggfunc=lambda x: x.iloc[0])
    df.columns = df.columns.get_level_values(1)
    return df.join(n)
