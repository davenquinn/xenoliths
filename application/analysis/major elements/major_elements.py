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

base_queryset = Point.objects.remove_bad()

output = []
for i,sample in enumerate(Sample.objects.all()):
	out = {
		"id": sample.id
	}


	sample_queryset = base_queryset.filter(sample=sample)
	print ""
	print sample.id

	sp = sample_queryset.filter(mineral="sp").distinct()
	cations = sp.get_cations()
	cr_ = cations["Cr"]/(cations["Cr"]+cations["Al"])*100
	print "Spinel Cr#: {0:4.1f}±{1:4.2f}".format(cr_.n, cr_.s)

	silicates = sample_queryset.filter(mineral__in=["cpx","opx","ol"]).distinct()
	cations = silicates.get_cations()
	mg_ = cations["Mg"]/(cations["Mg"]+cations["Fe"])*100
	print "Silicate Mg#: {0:4.1f}±{1:4.2f}".format(mg_.n, mg_.s)





