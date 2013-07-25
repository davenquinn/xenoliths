#!/usr/bin/env python

import numpy as N
import re
import IPython
import json
from affine import Affine
from django.contrib.gis.geos import GEOSGeometry
from samples import data,models
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def transform_coordinates(sample, records):
	dtype = [("point", int), ("x", float), ("y", float)]
	try:
		affine_seed = N.loadtxt(sample+"_affine.txt", delimiter="\t", comments="#", dtype=dtype)
	except IOError:
		print "No affine seed points available for "+sample
		return records

	fromCoords = []
	toCoords = []
	for a in affine_seed:
		idx = records['Line Numbers'] == a['point']
		point = records[idx][0]
		cord = [point[i+" Stage Coordinates (mm)"] for i in ["X","Y"]]
		tocord = [a["x"], a["y"]]
		print repr(cord)+" --> "+repr(tocord)
		fromCoords.append(cord)
		toCoords.append(tocord)

	affine = Affine.construct(fromCoords, toCoords, verbose=True)

	cords = N.transpose(N.vstack([records[i+" Stage Coordinates (mm)"] for i in ["X","Y"]]))
	outcords = affine.transform(cords)
	for i,a in enumerate(["X","Y"]):
		records[a+" Stage Coordinates (mm)"] = outcords[:,i]

	return records

def field_names(filename):
	with open(filename, "r") as f:
		field_names = f.readline()
		field_names = ' '.join(field_names.split()).replace('" "', ',').replace('"',"")
		field_names = field_names.split(",")
	#for f in field_names: print f
	return field_names

def get_array(sample_name, verbose=False):
	filename = sample_name+".dat"
	dtype = [(n,float) for n in field_names(filename)]
	if verbose: print field_names(filename)
	return N.loadtxt(filename, comments='"', dtype=dtype)	
		
def fix_cations(obj):
	a = 0
	for cat in settings.CATIONS:
		a += getattr(obj,cat)
	a += obj.O
	dif = a-obj.Total
	if N.abs(dif) > .0001:
		#print obj.id, dif
		obj.O = 4
		obj.save()

def import_sample(sample_name):
	arr = get_array(sample_name, False)

	arr = transform_coordinates(sample_name, arr)

	sample, created = models.Sample.objects.get_or_create(id=sample_name)

	for rec in arr:
		coords = [rec[a+" Stage Coordinates (mm)"] for a in "X Y".split()]
		wkt = "POINT({0} {1})".format(*coords)
		geom = GEOSGeometry(wkt)

		try:
			point = models.Point.objects.get(id=int(rec["Line Numbers"]))

		except ObjectDoesNotExist:
			point = models.Point(id=int(rec["Line Numbers"]),sample = sample)

		point.geometry = geom 

		for cation in settings.CATIONS:
			setattr(point,cation, rec[cation+" Formula Atoms"])
			setattr(point,cation+"_err", rec[cation+" Percent Errors"])

		point.O = 6

		point.Total = rec["Formula Totals"]
		for oxide in settings.OXIDES:
			setattr(point,oxide, rec[oxide+" Oxide Percents"])
		point.Ox_tot = rec["Oxide Totals"]
		point.save()
		fix_cations(point)


def import_all(delete=True):

	os.chdir(os.path.dirname(data.__file__))
	for sample in "CK-2 CK-3 CK-4".split():
		import_sample(sample)

if __name__ == "__main__":
	import_all()