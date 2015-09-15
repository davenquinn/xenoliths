# -*- coding: utf-8 -*-

from click import command, echo, style, secho

from .query import sims_data
from ..util import nested

minerals = dict(
    opx="Orthopyroxene",
    cpx="Clinopyroxene")

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

    data = sims_data(exclude_bad=False)

    print_data(data)
