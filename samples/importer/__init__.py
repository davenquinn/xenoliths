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

def import_sample(sample_name):
	arr = Array(sample_name+".dat")

	arr.transform_coordinates(sample_name+"_affine.txt")

	sample, created = models.Sample.objects.get_or_create(id=sample_name)

	for rec in arr.each():
		uid = "_".join((sample_name,str(int(rec.id))))
		try:
			point = models.Point.objects.get(uid=uid)
		except ObjectDoesNotExist:
			point = models.Point(uid=uid, id=int(rec.id),sample = sample)

		point.geometry = rec.geometry()
		point.oxides = rec.oxide_weights()
		point.errors = rec.errors()
		if point.oxides["Total"] < 85:
			point.bad = True
		point.save(compute_parameters=True)

def import_all(delete=True):

	os.chdir(os.path.dirname(data.__file__))
	for sample in settings.SAMPLES:
		import_sample(sample)

if __name__ == "__main__":
	import_all()