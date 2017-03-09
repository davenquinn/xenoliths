# -*- coding:utf-8 -*-



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

def single_measurement(queryset, method=Taylor1998, **kwargs):
    opx = queryset.filter(ProbeMeasurement.mineral=="opx")
    cpx = queryset.filter(ProbeMeasurement.mineral=="cpx")
    thermometer = method(opx,cpx, **kwargs)
    return {
        "val": thermometer.temperature(),
        "n_opx": opx.count(),
        "n_cpx": cpx.count()
    }

def closest(a,b, distinct=None):
    def columns(i):
        try:
            return i.c
        except AttributeError:
            return i

    a = columns(a)
    b = columns(b)

    if distinct is None:
        distinct = a
    distinct = columns(distinct)

    dist = func.ST_Distance(a.geometry,b.geometry)
    return select(
        [a.id, b.id],
        a.id != b.id,
        distinct=distinct.id,
        order_by=[distinct.id, dist],
        use_labels=True)

def pyroxene_pairs(queryset, distinct=min,names=("opx","cpx")):
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

def separate_measurements(pairs, method=Taylor1998, **kwargs):
    return [method(*a, **kwargs).temperature() for a in pairs]

def core_temperatures(sample, method=Taylor1998, **kwargs):
    queryset = exclude_bad(ProbeMeasurement.query.filter_by(sample=sample))
    queryset = tagged(queryset, "core")
    pairs = pyroxene_pairs(queryset,**kwargs)
    return separate_measurements(pairs, method=method)

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
    bkn = BKN(opx, cpx)
    T = bkn.temperature()
    return T,Ca_Olivine(ol, cpx, bkn).pressure()

def sample_temperatures(sample, **kwargs):
    base_queryset = exclude_bad(ProbeMeasurement.query)
    sample_queryset = base_queryset.filter(ProbeMeasurement.sample==sample)

    def type_results(typeid="core"):
        queryset = tagged(sample_queryset, typeid)
        pairs = pyroxene_pairs(queryset, distinct=kwargs.pop('distinct',None))
        for tname, thermometer in thermometers.items():
            sep = separate_measurements(pairs, method=thermometer, **kwargs)
            T = N.array(sep)
            yield tname, dict(
                sep = T,
                single = single_measurement(queryset, method=thermometer, **kwargs))
    s = {i:{k:v for k,v in type_results(i)} for i in ("core","rim")}
    s["id"] = sample.id
    s["color"] = sample.color
    return s

