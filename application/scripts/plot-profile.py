#!/usr/bin/env python
"""
Plots a profile across a clinopyroxene grain.
"""

from os import path, makedirs
import errno
import seaborn as sns
from matplotlib import pyplot as P
from xenoliths.application import app
from xenoliths.models import ProbeMeasurement

def mkdir(n):
    try:
        makedirs(n)
    except OSError as exc:
        if exc.errno == errno.EEXIST and path.isdir(n):
            pass
        else: raise

here = path.dirname(path.abspath(__file__))

res = path.join(here,"../data/results/cpx-profile")
mkdir(res)

with app.app_context():
    measurements = ProbeMeasurement.query\
        .filter(ProbeMeasurement.sample_id == "CK-1")\
        .filter(ProbeMeasurement.line_number >= 176)\
        .filter(ProbeMeasurement.line_number <= 201)\
        .order_by(ProbeMeasurement.line_number)

    meas = measurements.all()
    ids = [i.line_number for i in meas]
    cats = [i.get_cations() for i in meas]
    for cat in cats:
        cat["mg_number"]=cat["Mg"]/(cat["Mg"]+cat["Fe"])

    for cat in list(cats[0].keys()):
        n = [c[cat].n for c in cats]

        fig, ax = P.subplots()
        ax.plot(ids,n)
        ax.set_xlabel("Measurement ID")
        ax.set_ylabel(cat+" formula cations")
        fig.savefig(path.join(res,cat+".pdf"),format="pdf")
