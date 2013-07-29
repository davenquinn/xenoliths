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
		try:
			point = models.Point.objects.get(id=rec.id)
		except ObjectDoesNotExist:
			point = models.Point(id=int(rec.id),sample = sample)

		point.geometry = rec.geometry()
		point.oxides = rec.oxide_weights()
		point.errors = rec.errors()
		point.save(compute_parameters=True)

def import_all(delete=True):

	os.chdir(os.path.dirname(data.__file__))
	for sample in "CK-2 CK-3 CK-4".split():
		import_sample(sample)

if __name__ == "__main__":
	import_all()