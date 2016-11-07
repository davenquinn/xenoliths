#!/usr/bin/env python
from __future__ import division
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from samples.models import Sample,Point
from samples.thermometry import temperature, remove_bad
from samples.thermometry.thermometers import Taylor1998, Ca_OPX_Corr
import matplotlib.pyplot as P
import numpy as N


def cr_number(queryset):
	def generate(queryset):
		for point in queryset:
			yield point.params["Cr#"]
	queryset = remove_bad(queryset).filter(tags__name__in=["core"])
	ls = list(generate(queryset.filter(mineral="sp").distinct()))
	return sum(ls)/len(ls)


def generate_data():
	for sample in Sample.objects.all():
		queryset = Point.objects.filter(sample=sample)
		yield {
			"temp": temp(queryset),
			"name": sample.id,
			"Cr#": cr_number(queryset)
		}

temp = lambda q: temperature(q, type="core", thermometer=Ca_OPX_Corr)

data = list(generate_data())

annotate_props = dict(xytext=(5,-5), textcoords='offset points', ha='left', va='center')
fig = P.figure()
ax = fig.add_subplot(111)
x = [a["temp"] for a in data]
y = [a["Cr#"] for a in data]
ax.scatter(x,y,zorder=10, marker="o")
for a in data:
	ax.annotate(a["name"], xy=(a["temp"],a["Cr#"]), **annotate_props)

ax.set_xlabel(u"Ca-in-OPX \u00b0C ")
ax.set_ylabel(u"Cr#")

fig.suptitle("Cr# vs. Ca-in-OPX core (P = 1.5 GPa)")
path = os.path.join("output", "cr#_ca-opx.svg")
fig.savefig(path, bbox_inches="tight")

