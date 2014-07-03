#!/usr/bin/env python

import numpy as N
from django.contrib.gis.geos import GEOSGeometry
from samples.quality import data_quality
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from ..models import Sample, Point
from .array import Array

def get_or_create(model, *args, **kwargs):
	return model.query.get(*args, **kwargs), False


def import_sample(sample_name):
	arr = Array(sample_name+".dat")

	arr.transform_coordinates(sample_name+"_affine.txt")

	sample, created = get_or_create(Sample,id=sample_name)

	for rec in arr.each():
		try:
			point = models.Point.query.get(line_number=int(rec.id), sample=sample)
		except ObjectDoesNotExist:
			point = models.Point(n=int(rec.id),sample = sample)

		point.geometry = rec.geometry()
		point.oxides = rec.oxide_weights()
		point.errors = rec.errors()
		point.save()
		point.save(compute_parameters=True)
		#data_quality(point)


def import_all(delete=True):
	os.chdir(os.path.join(settings.SITE_DIR,"data","samples"))
	for sample in settings.SAMPLES:
		print sample
		import_sample(sample)
	views.write_json()

if __name__ == "__main__":
	import_all()
