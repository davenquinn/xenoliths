# -*- coding:utf-8 -*-

from __future__ import division

from flask import app

import numpy as N
import pandas as P

from uncertainties import ufloat
from functools import partial
from itertools import chain
from sqlalchemy.sql import func, select
from sqlalchemy.orm import aliased

from ..models import Sample, ProbeMeasurement
from ..application import db
from ..microprobe.models.query import tagged, exclude_bad
from .thermometers import BKN, Taylor1998, Ca_OPX, Ca_OPX_Corr
from .barometers import Ca_Olivine

def serializable(ufloat):
    return {
        "v": ufloat.nominal_value,
        "s": ufloat.std_dev
    }

thermometers = {
    "ta98": Taylor1998,
    "bkn": BKN,
    "ca_opx": Ca_OPX,
    "ca_opx_corr": Ca_OPX_Corr
}

#pressure = ufloat(1.5, 0.2, "pressure")

#base_queryset = ProbeMeasurement.query.filter()

def single_measurement(queryset, method=Taylor1998):
    opx = queryset.filter(ProbeMeasurement.mineral=="opx")
    cpx = queryset.filter(ProbeMeasurement.mineral=="cpx")
    thermometer = method(opx,cpx, uncertainties=True)
    return {
        "val": thermometer.temperature(),
        "n_opx": opx.count(),
        "n_cpx": cpx.count()
    }

def closest(a,b, distinct=None):

    if distinct is None:
        distinct = a
    distinct = distinct.c.id

    dist = func.ST_Distance(a.c.geometry,b.c.geometry)
    return select(
        [a.c.id, b.c.id],
        a.c.id != b.c.id,
        distinct=distinct,
        order_by=[distinct, dist],
        use_labels=True)

def pyroxene_pairs(queryset, distinct=min):
    names = ("opx","cpx")
    opx,cpx = (queryset
                .filter(ProbeMeasurement.mineral==a)
                .subquery() for a in names)
    # Restrict number selected to minimum or maximum number of measurements
    # to avoid duplication
    if distinct:
        distinct = distinct((opx,cpx),key=lambda d: d.count())
    q = closest(opx,cpx, distinct=distinct)
    res = db.session.execute(q).fetchall()
    return tuple(
        tuple(ProbeMeasurement.query.get(i) for i in pair)
        for pair in res)

def separate_measurements(pairs, method=Taylor1998):
    return [method(*a, uncertainties=False).temperature() for a in pairs]

def core_temperatures(sample, method=Taylor1998):
    queryset = exclude_bad(ProbeMeasurement.query.filter_by(sample=sample))
    queryset = tagged(queryset, "core")
    return separate_measurements(queryset, method=method)

def xenoliths():
    return Sample.query\
        .filter(Sample.xenolith==True)\
        .order_by(Sample.id)\
        .all()

def core_pressures(sample):
    queryset = ProbeMeasurement.query.filter_by(sample=sample)
    queryset = tagged(exclude_bad(queryset), "core")
    ol = queryset.filter(ProbeMeasurement.mineral=="ol")
    opx = queryset.filter(ProbeMeasurement.mineral=="opx")
    cpx = queryset.filter(ProbeMeasurement.mineral=="cpx")
    T = BKN(opx, cpx).temperature()
    return T,Ca_Olivine(ol, cpx).pressure(T)

def sample_temperatures(sample, **kwargs):
    base_queryset = exclude_bad(ProbeMeasurement.query)
    sample_queryset = base_queryset.filter(ProbeMeasurement.sample==sample)

    def type_results(typeid="core"):
        queryset = tagged(sample_queryset, typeid)
        pairs = pyroxene_pairs(queryset, **kwargs)
        for tname, thermometer in thermometers.iteritems():
            sep = separate_measurements(pairs, method=thermometer)
            T = N.array(sep)
            yield tname, dict(
                sep = T,
                single = single_measurement(queryset, method=thermometer))
    s = {i:{k:v for k,v in type_results(i)} for i in ("core","rim")}
    s["id"] = sample.id
    s["color"] = sample.color
    return s

