#!/usr/bin/env python
from __future__ import division
from django.conf import settings

from samples.models import Sample,Point
from thermometers import Taylor1998

import numpy as N

pressure = 1.5

bad_tags = [
	"bad",
	"alteration",
	"mixed",
	"marginal",
	"anomalous",
	"review",
	"near alteration"
]

def remove_bad(queryset):
	return queryset.exclude(tags__name__in=bad_tags)

def temperature(queryset, thermometer=Taylor1998, type=None, pressure=1.5, uncertainties=False):
	queryset = remove_bad(queryset)
	if type is not None:
		queryset = queryset.filter(tags__name__in=[type])

	opx = queryset.filter(mineral="opx").distinct()
	cpx = queryset.filter(mineral="cpx").distinct()

	thermometer = thermometer(opx,cpx, uncertainties=uncertainties)
	return thermometer.temperature(pressure=pressure)

def aggregate_errors(T, combine_bases=[]):
	"""Quadratic sum of errors with same tag. Provides contribution to total error."""
	errors = {}
	for var, error in T.error_components().iteritems():
		tag = var.tag
		for base in combine_bases:
			if base in var.tag:
				tag = base
				break
		errors[tag] = errors.get(tag,0) + error**2
	for tag,error in errors.iteritems():
		errors[tag] = error**.5
	return errors

