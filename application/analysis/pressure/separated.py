#!/usr/bin/env python
# -- coding: utf-8 --


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.contrib.gis.geos import *

import json
import numpy as N
import IPython

from uncertainties import ufloat
from django.conf import settings

from samples.models import Sample, Point
from samples.thermometry.thermometers import BKN, Taylor1998

from samples.thermometry.barometers import Ca_Olivine
from samples.geotherm import HeatFlowModel


def geobaric_gradient(depth):
	return depth*.03 #GPa/km
def depth(pressure):
	return pressure/.03

model = HeatFlowModel(q_0=90)

pressure = ufloat(1.5, 0.2, "pressure")
base_queryset = Point.objects.remove_bad()

def measurement(ol, opx, cpx):
	ta98 = Taylor1998(opx,cpx).temperature(pressure=pressure).n
	bkn = BKN(opx,cpx).temperature(pressure=pressure).n
	P_ol = Ca_Olivine(ol,cpx).pressure(bkn).n
	z_md = model.get_depth(ta98)[0]
	try:
		sample = ol.sample.id
	except AttributeError:
		sample = ol[0].sample.id
	return {
		"sample": sample,
		"olivine": {
			"P": P_ol,
			"z": depth(P_ol)
			},
		"heatflow": {
			"P": geobaric_gradient(z_md),
			"z": z_md
			},
		"T_bkn": bkn,
		"T_ta98": ta98
		} 


def single_measurement(queryset):
	ol = queryset.filter(mineral="ol").distinct()
	opx = queryset.filter(mineral="opx").distinct()
	cpx = queryset.filter(mineral="cpx").distinct()
	return measurement(ol,opx,cpx)

def separate_measurements(queryset):
	ol = queryset.filter(mineral="ol").distinct()
	opx = queryset.filter(mineral="opx").distinct()
	cpx = queryset.filter(mineral="cpx").distinct()
	for single_ol in ol:
		single_opx = opx.distance(single_ol.geometry).order_by("-distance")[0]
		single_cpx = cpx.distance(single_ol.geometry).order_by("-distance")[0]
		yield measurement(single_ol,single_opx,single_cpx)

queryset = base_queryset.filter(tags__name__in=["core"])

res = {
	"single": [],
	"multiple": []
}
for sample in Sample.objects.all():
	sample_queryset = queryset.filter(sample=sample)
	res["single"] += [single_measurement(sample_queryset)]
	mult = list(separate_measurements(sample_queryset))
	res["multiple"] += mult

	print(sample.id)
	pressures = N.array([i["olivine"]["P"] for i in mult])
	print("{0:.2f}±{1:.2f} GPa".format(pressures.mean(),pressures.std()))
	depths = N.array([i["olivine"]["z"] for i in mult])
	print("{0:.2f}±{1:.2f} km".format(depths.mean(),depths.std()))


path = os.path.join(os.path.dirname(os.path.abspath( __file__ )), "separated.json")
with open(path, "w") as f:
	json.dump(res, f)




