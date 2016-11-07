#!/usr/bin/env python
# -- coding: utf-8 --

from __future__ import division
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.contrib.gis.geos import *

import json
import numpy as N
import IPython

from uncertainties import ufloat
from django.conf import settings

from samples.models import Sample, Point
from samples.thermometry import aggregate_errors
from samples.thermometry.thermometers import Taylor1998, BKN
from samples.thermometry.barometers import Ca_Olivine
from samples.thermometry.geotherm import HeatFlowModel


def serializable(ufloat):
	return {
		"v": ufloat.nominal_value,
		"s": ufloat.std_dev
	}

pressure = ufloat(1.5, 0.2, "pressure")

base_queryset = Point.objects.remove_bad()

def geobaric_gradient(depth):
	return depth*.03 #GPa/km

model = HeatFlowModel(q_0=90)


output = []
for i,sample in enumerate(Sample.objects.all()):
	queryset = base_queryset.filter(sample=sample, tags__name__in=["core"])
	print sample.id
	print "Core"
	opx = queryset.filter(mineral="opx").distinct()
	cpx = queryset.filter(mineral="cpx").distinct()
	ol = queryset.filter(mineral="ol").distinct()
	thermo1 = Taylor1998(opx,cpx, uncertainties=True)
	thermometer = BKN(opx,cpx, uncertainties=True)
	TA98 = thermo1.temperature(pressure=1.5)
	temp = thermometer.temperature(pressure=1.5)
	barometer = Ca_Olivine(ol,cpx, uncertainties=True)
	pressure = barometer.pressure(temp)

	p_geo = geobaric_gradient(model.get_depth(TA98.n)[0])

	print "T: {0:.2f}±{1:.2f}ºC (Taylor, 1998)".format(TA98.n,TA98.s)
	print "   {0:.2f}±{1:.2f}ºC (Brey and Köhler, 1990) [used for pressure calculation]".format(temp.n,temp.s)
	print "P: {0:.2f} GPa (TA98 pinned to 90mW/m2 geothermal gradient)".format(p_geo)
	print "   {0:.2f} GPa (Köhler and Brey, 1990)".format(pressure)
	out = {
		"id": sample.id,
		"T":  temp.n,
		"P_ca": pressure,
		"P_geo": p_geo
	}
	output.append(out)
	errors = aggregate_errors(pressure, combine_bases=["probe"])
	print "   Errors"
	for (tag, error) in errors.items():
		print u"-  {0}: {1:.2f}".format(tag, error)
	print ""


#path = os.path.join(os.path.dirname(os.path.abspath( __file__ )), "results.json")
#with open(path, "w") as f:
#	#json.dump(output, f)





