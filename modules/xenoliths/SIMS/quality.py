# -*- coding: utf-8 -*-

from sqlalchemy import func
from click import command, echo, style, secho
from periodictable import elements
from collections import OrderedDict

from ..application import db
from ..util import uval, nested
from ..models import Sample
from .models import SIMSMeasurement as meas
from .models import SIMSDatum as datum

minerals = dict(
    opx="Orthopyroxene",
    cpx="Clinopyroxene")

def get_data(exclude_bad=True):
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
        d = [uval(*i) for i in zip(u,th)]
        out[s][m][el] = d
    return out

def test_meas(measurements, level=1):
    """ Tests agreement at the specificed
        standard-deviation level.
    """
    ranges = [[i.n-level*i.s, i.n+level*i.s]\
        for i in measurements]

    def comparator(i,j):
        if i[0] < j[0]:
            i[0] = j[0]
        if i[1] > j[1]:
            i[1] = j[1]
        return i
    out = reduce(comparator, ranges)
    return True if out[0] <= out[1] else False

@nested(lambda k,v: "Sample "\
    +style(k, fg="cyan", bold=True))
@nested(lambda k,v: "{0}: {1} measurements"\
    .format(minerals[k],len(v["Nd"])))
def print_data(meas):
    echo("Agreement at")
    for lev in range(1,10):
        echo("- {0}σ: ".format(lev),
            nl=False)
        for el,m in meas.items():
            t = test_meas(m, lev)
            color = "green" if t else "red"
            sel = style(" {0} ".format(el), fg="black",bg=color)
            echo(sel, nl=False)
        echo("")
    echo("")

@command(name="check-quality")
def check_quality():
    """ Checks integrity of SIMS data"""
    echo(""" This checks the between-measurement
    correspondence of trace-element data for areas
    within the same sample.""")

    data = get_data(exclude_bad=False)

    print_data(data)
