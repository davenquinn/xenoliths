#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from samples.models import Sample
from django.conf import settings
import numpy as N

from project_options import minerals

def build_array(dataset):
	shape = (int(dataset['h']),int(dataset['w']))
	arr = N.array([d["v"] for d in dataset["values"]]).reshape(*shape)
	arr[arr == "un"] = "na"
	return arr

densities = {
	"cpx": 3.279,
	"opx": 3.204,
	"ol": 3.21,
	"sp": 3.6,
	"al": 3.23
} # These are very approximate!

query = Sample.objects.all().order_by("id")
for sample in query:
	arr = build_array(sample.classification)
	T = arr.size
	print("")
	area = {}
	print("{0:20s}".format(sample.id)+" Area % "+"  Vol % "+"  Wt %  ")
	for m, item in list(minerals.items()):
		mode = arr[arr == m].size/T
		if m == "na":
			na = mode
			continue
		area[m] = mode
	print("{} pixels".format(T))

	vol = {}
	for m, item in list(area.items()):
		vol[m] = item**1.5
	total = sum(vol.values())
	for m, item in list(vol.items()):
		vol[m] = item/total

	wt = {}
	for m, item in list(vol.items()):
		wt[m] = item*densities[m]
	total = sum(wt.values())
	for m,item in list(wt.items()):
		wt[m] = item/total



	for m, item in list(minerals.items()):
		if m == "na": continue
		print("{0:20s}{1:8.3f}{2:8.3f}{3:8.3f}".format(item["name"],100*area[m],100*vol[m], 100*wt[m]))
	print("{0:20s}{1:8.3f}".format("None",na*100))
	print("")
	print("")