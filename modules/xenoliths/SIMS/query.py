import numpy as N
from sqlalchemy import func
from periodictable import elements
from collections import OrderedDict

from ..application import db
from ..util import uval
from .models import SIMSMeasurement as meas
from .models import SIMSDatum as datum

def sims_data(exclude_bad=True, averaged=False):
    """
    Gets trace element data grouped by sample and
    minerals. The data is formatted as a nested ordered
    dictionary, for iterability. This data can be used
    as-is or averaged, as appropriate.
    """
    vals = [meas.sample_id,
            meas.mineral,
            datum.element]
    qvars = vals+[
        func.array_agg(datum.norm_ppm),
        func.array_agg(datum.norm_std)]

    if exclude_bad:
        bad_data = datum.bad.isnot(True)
    else:
        # A meaningless filter
        bad_data = True

    data = (db.session.query(datum)
        .filter(datum.element != 14)
        .filter(bad_data)
        .join(meas)
        .with_entities(*qvars)
        .group_by(*vals)
        .order_by(*vals)
        .all())

    out = OrderedDict()
    for s,m,e,u,th in data:
        # Create data structure
        el = elements[e].symbol
        if s not in out:
            out[s] = {}
        if m not in out[s]:
            out[s][m] = OrderedDict()
        # Add data
        # We make sure to standardize away negative values.
        d = [uval(*i) for i in zip(N.abs(u),N.abs(th))]
        if averaged:
            d = N.mean(d)
        out[s][m][el] = d
    return out
