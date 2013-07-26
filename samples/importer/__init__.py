#!/usr/bin/env python

import numpy as N
import re
import IPython
from array import Array
from django.contrib.gis.geos import GEOSGeometry
from samples import data,models
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

def fix_cations(sample_name, obj):
	filename = sample_name+".dat"
	with open(filename, "r") as f:
		field_names = f.readline()
		field_names = ' '.join(field_names.split()).replace('" "', ',').replace('"',"")
		field_names = field_names.split(",")

	dtype = [(n,float) for n in field_names]
	return N.loadtxt(filename, comments='"', dtype=dtype)
	a = 0
	for cat in settings.CATIONS:
		a += obj.get(cat)
	a += obj.O
	dif = a-obj.Total
	if N.abs(dif) > .0001:
		#print obj.id, dif
		obj.O = 4
		obj.save()

def import_sample(sample_name):
	arr = Array(sample_name+".dat")

	arr.transform_coordinates(sample_name+"_affine.txt")

	sample, created = models.Sample.objects.get_or_create(id=sample_name)

	for rec in arr.each():
		try:
			point = models.Point.objects.get(id=rec.id)
		except ObjectDoesNotExist:
			point = models.Point(id=int(rec.id),sample = sample)

		point.geometry = rec.geometry()

		for cation in settings.CATIONS:
			setattr(point,cation, rec.get(cation+" Formula Atoms"))
			setattr(point,cation+"_err", rec.get(cation+" Percent Errors"))

		point.O = 6

		point.Total = rec.get("Formula Totals")
		for oxide in settings.OXIDES:
			setattr(point,oxide, rec.get(oxide+" Oxide Percents"))
		point.Ox_tot = rec.get("Oxide Totals")
		point.save()
		fix_cations(sample_name, point)


def import_all(delete=True):

	os.chdir(os.path.dirname(data.__file__))
	for sample in "CK-2 CK-3 CK-4".split():
		import_sample(sample)

if __name__ == "__main__":
	import_all()