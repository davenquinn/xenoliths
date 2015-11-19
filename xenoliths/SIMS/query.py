import numpy as N
import pandas as P
from sqlalchemy import func
from periodictable import elements
from collections import OrderedDict

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
        .with_entities(
            meas.sample_id,
            meas.mineral,
            datum.element,
            datum.norm_ppm,
            datum.norm_std))

    df = P.read_sql(q.statement,q.session.bind)
    fn = lambda row: uval(
            row['norm_ppm'],
            row['norm_std'])
    df['norm'] = df.apply(fn,axis=1)
    df = (df
        .drop('norm_ppm', axis=1)
        .drop('norm_std', axis=1))

    g = df.groupby(['sample_id','mineral','element'])
    if averaged:
        df = g['norm'].agg(lambda r: N.mean(r.values))

    if dataframe:
        return df

    if not averaged:
        df = g['norm'].agg(lambda r: tuple(r.values))

    out = OrderedDict()
    for (s,m,e),n in df.iteritems():
        # Create data structure
        el = elements[e].symbol
        if s not in out:
            out[s] = {}
        if m not in out[s]:
            out[s][m] = OrderedDict()
        out[s][m][el] = n
    return out
