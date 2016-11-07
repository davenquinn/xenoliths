#!/usr/bin/env python
from __future__ import division
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import json
import matplotlib.pyplot as P
import numpy as N
import IPython

from uncertainties import ufloat
from django.conf import settings

from samples.models import Sample, Point
from samples.thermometry import Taylor1998, aggregate_errors

def serializable(ufloat):
	return {
		"v": ufloat.nominal_value,
		"s": ufloat.std_dev
	}

pressure = ufloat(1.5, 0.2, "pressure")

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
		"pressure": serializable(pressure)
	},
	"samples": []
}

for sample in Sample.objects.all():
	dct = {
		"core": {},
		"rim": {}
	}
	sample_queryset = base_queryset.filter(sample=sample)
	print ""
	print sample.id
	for a_type, a_dict in dct.items():
		queryset = sample_queryset.filter(tags__name__in=[a_type])


		opx = queryset.filter(mineral="opx").distinct()
		cpx = queryset.filter(mineral="cpx").distinct()

		thermometer = Taylor1998(opx,cpx, uncertainties=True)
		T = thermometer.temperature(pressure=pressure)

		errors = aggregate_errors(T, combine_bases=["probe"])
		print u" \n## {0:.2fP}\n".format(T)

		a_dict["T"] = T.nominal_value
		a_dict["errors"] = {
			"Total": T.std_dev
		}

		for (tag, error) in errors.items():
			print u"- {0}: {1:.2f}".format(tag, error)
			a_dict["errors"][tag] = error

	dct["id"] = sample.id
	output["samples"].append(dct)


path = os.path.join(os.path.dirname(os.path.abspath( __file__ )), "data.json")
with open(path, "w") as f:
	json.dump(output, f, sort_keys=True,
		indent=4, separators=(',', ': '))

