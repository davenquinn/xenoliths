# -*- coding:utf-8 -*-

from __future__ import division

from flask import app

import numpy as N

from uncertainties import ufloat
from functools import partial

from ..models import Sample, Point
from ..microprobe.models.point.query import tagged, exclude_bad
from .thermometers import BKN, Taylor1998, Ca_OPX, Ca_OPX_Corr

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

#base_queryset = Point.query.filter()

def single_measurement(queryset, method=Taylor1998):
    opx = queryset.filter(Point.mineral=="opx").all()
    cpx = queryset.filter(Point.mineral=="cpx").all()
    thermometer = method(opx,cpx, uncertainties=True)
    return {
        "val": thermometer.temperature(),
        "n_opx": len(opx),
        "n_cpx": len(cpx)
    }

def closest(queryset, measurement):
    return queryset.order_by(Point.geometry.distance_centroid(measurement.geometry)).first()

def pyroxene_pairs(queryset):
    all_opx = queryset.filter(Point.mineral=="opx")
    all_cpx = queryset.filter(Point.mineral=="cpx")
    if all_opx.count() < all_cpx.count():
        return [(closest(all_opx, c),c) for c in all_cpx.all()]
    else:
        return [(o,closest(all_cpx, o)) for o in all_opx.all()]

def separate_measurements(queryset, method=Taylor1998):
    pairs = pyroxene_pairs(queryset)
    return [method(*a, uncertainties=False).temperature() for a in pairs]

def text_output():
    base_queryset = exclude_bad(Point.query)
    for sample in Sample.query.all():
        sample_queryset = base_queryset.filter(Point.sample==sample)
        print sample.id
        for typeid in ["core", "rim"]:
            queryset = tagged(sample_queryset, typeid)
            print queryset.count()
            for tname, thermometer in thermometers.iteritems():
                res = separate_measurements(queryset, method=thermometer)
                if len(res) == 0: continue
                T = N.array(res)
                print "{1} - {0}".format(typeid, thermometer.name)
                print "Separate: {0:7.2f}±{1:5.2f} ºC".format(T.mean(), T.std())
                print "  N = {0} pairs".format(len(T))
                print "  min: {0:7.2f}, max: {1:7.2f}".format(T.min(), T.max())

                single = single_measurement(queryset, method=thermometer)
                print "En-masse: {0:7.2f}ºC".format(single["val"])
                print "  N = {0:2.0f} opx, {1:2.0f} cpx".format(single["n_opx"],single["n_cpx"])
                print ""

def core_temperatures(sample, method=Taylor1998):
    queryset = exclude_bad(Point.query.filter_by(sample=sample))
    queryset = tagged(queryset, "core")
    res = separate_measurements(queryset, method=thermometer)
