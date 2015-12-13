import numpy as N
from pandas import read_sql, MultiIndex, pivot_table
from sqlalchemy import func
from periodictable import La,Lu,elements

from ..application import db
from ..util import uval
from .models import SIMSMeasurement as meas
from .models import SIMSDatum as datum

def sims_data(**kwargs):
    """
    Gets trace element data grouped by sample and
    minerals. The data is formatted as a nested ordered
    dictionary, for iterability. This data can be used
    as-is or averaged, as appropriate.
    """

    exclude_bad = kwargs.pop('exclude_bad',True)
    averaged = kwargs.pop('averaged',False)
    dataframe = kwargs.pop('dataframe',False)

    if exclude_bad:
        bad_data = datum.bad.isnot(True)
    else:
        # A meaningless filter
        bad_data = True

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
            func.array_agg(datum.norm_ppm)
                .label('norm_ppm'),
            func.array_agg(datum.norm_std)
                .label('norm_std'),
            func.count(datum.norm_ppm)
                .label('n')))

    df = read_sql(q.statement,q.session.bind)

    # Apply uncertainty
    def uncertainty(row):
        vals = zip(row['norm_ppm'],row['norm_std'])
        return [uval(n,s) for n,s in vals]

    df['norm'] = df.apply(uncertainty,axis=1)
    df = (df
        .drop('norm_ppm', axis=1)
        .drop('norm_std', axis=1))

    fn = lambda x: elements[x['element']].symbol
    df['symbol'] = df.apply(fn, axis=1)
    df['average'] = df['norm'].apply(N.mean)

    names = ('sample_id','mineral','element','symbol')
    df.index = MultiIndex.from_arrays(
        [df.pop(i) for i in names])
    df.sortlevel(inplace=True)
    return df

def ree_only(df):
    ix = df.index.names.index('element')
    is_ree = lambda n: La.number <= n[ix] <= Lu.number
    return df[df.index.map(is_ree)]

