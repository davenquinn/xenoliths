# -*- coding:utf-8 -*-

from __future__ import division

from flask import app

import numpy as N

from uncertainties import ufloat

from ..models import Sample, Point
from ..microprobe.models.point.query import exclude_bad
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
	opx = queryset.filter(mineral="opx").distinct()
	cpx = queryset.filter(mineral="cpx").distinct()
	thermometer = method(opx,cpx, uncertainties=True)
	return {
		"val": thermometer.temperature(pressure=pressure).n,
		"n_opx": len(opx),
		"n_cpx": len(cpx)
	}

def closest(measurement, queryset):
	return queryset.distance(measurement.geometry).order_by("-distance")[0]

def separate_measurements(queryset, method=Taylor1998):
	all_opx = queryset.filter(mineral="opx").distinct()
	all_cpx = queryset.filter(mineral="cpx").distinct()
	if len(all_opx) < len(all_cpx):
		for single_cpx in cpx:
			single_opx = closest(single_cpx,opx)
			thermometer = method(single_opx,single_cpx, uncertainties=True)
			yield thermometer.temperature(pressure=pressure).n
	else:
		cpx
		for single_opx in opx:
			single_cpx = closest(single_opx,cpx)
			thermometer = method(single_opx,single_cpx, uncertainties=True)
			yield thermometer.temperature(pressure=pressure).n

def text_output():
	base_queryset = exclude_bad(Point.query)

	for i,sample in enumerate(Sample.query.all()):
		out = {
			"id": sample.id
		}


		sample_queryset = base_queryset.filter(sample=sample)
		print ""
		print sample.id
		for typeid in ["core", "rim"]:
			out[typeid] = {}
			queryset = sample_queryset.filter(tags__name__in=[typeid])
			for tname, thermometer in thermometers.iteritems():
				T = N.array(list(separate_measurements(queryset, method=thermometer)))
				print "{1} - {0}".format(typeid, thermometer.name)
				print "Separate: {0:7.2f}ºC ± {1:5.2f}".format(T.mean(), T.std())
				print "  N = {0} pairs".format(len(T))
				print "  min: {0:7.2f}, max: {1:7.2f}".format(T.min(), T.max())

				single = single_measurement(queryset, method=thermometer)
				print "En-masse: {0:7.2f}ºC".format(single["val"])
				print "  N = {0:2.0f} opx, {1:2.0f} cpx".format(single["n_opx"],single["n_cpx"])
				print ""
				out[typeid][tname] = {
					"separate": {
						"values": list(T),
						"n": len(T),
						"µ": T.mean(),
						"s": T.std(),
						"min": T.min(),
						"max": T.max()
					},
					"grouped": single
				}
		output.append(out)
