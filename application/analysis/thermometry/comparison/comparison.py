#!/usr/bin/env python
from __future__ import division
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import IPython
from django.conf import settings
import json
from uncertainties import ufloat
from samples.models import Sample,Point
from samples.group import Group
from samples.thermometry import BKN, Taylor1998, Ca_OPX, Ca_OPX_Corr, aggregate_errors

import matplotlib.pyplot as P
import numpy as N

def header(text):
	print text
	print "="*len(text)

systems = {
	"bkn": BKN,
	"ta98": Taylor1998,
	"ca_opx": Ca_OPX,
	"ca_opx_corr": Ca_OPX_Corr
}

pressure = 1.5

tags = [
	"bad",
	"alteration",
	"mixed",
	"marginal",
	"anomalous",
	"review",
	"near alteration"
]

base_queryset = Point.objects.exclude(tags__name__in=tags)

output = {
	"config": {
		"pressure": 1.5
	},
	"samples": {}
}

for sample in Sample.objects.all():
	output["samples"][sample.id] = {
		"core": {},
		"rim": {}
	}
	sample_queryset = base_queryset.filter(sample=sample)
	print ""
	print sample.id
	for a_type, a_dict in output["samples"][sample.id].items():
		queryset = sample_queryset.filter(tags__name__in=[a_type])
		for pt in queryset:
			print pt.id, ", ".join([tag.name for tag in pt.tags.all()])
		opx = queryset.filter(mineral="opx").distinct()
		cpx = queryset.filter(mineral="cpx").distinct()

		for name, system in systems.items():
			thermometer = system(opx,cpx, uncertainties=False)
			a_dict[name] = thermometer.temperature(pressure=pressure)


path = os.path.join(os.path.dirname(os.path.abspath( __file__ )), "data.json")
with open(path, "w") as f:
	json.dump(output, f)
