#!/usr/bin/env python

import numpy as N
import re
import IPython
from array import Array
from django.contrib.gis.geos import GEOSGeometry
from samples import data,models,views
from samples.quality import data_quality
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def import_sample(sample_name):
	arr = Array(sample_name+".dat")

	arr.transform_coordinates(sample_name+"_affine.txt")

	sample, created = models.Sample.objects.get_or_create(id=sample_name)

	for rec in arr.each():
		try:
			point = models.Point.objects.get(n=int(rec.id), sample=sample)
		except ObjectDoesNotExist:
			point = models.Point(n=int(rec.id),sample = sample)

		point.geometry = rec.geometry()
		point.oxides = rec.oxide_weights()
		point.errors = rec.errors()
		point.save()
		point.save(compute_parameters=True)
		#data_quality(point)


def import_all(delete=True):
	os.chdir(os.path.join(SITE_DIR,"data","samples"))
	for sample in settings.SAMPLES:
		print sample
		import_sample(sample)
	views.write_json()

if __name__ == "__main__":
	import_all()
