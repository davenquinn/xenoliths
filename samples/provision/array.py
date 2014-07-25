import numpy as N
import json
import os
from shapely.geometry import Point

from .affine import Affine
from ..application import app

class Array(object):
	"""A wrapper around a .dat file obtained for the electron microprobe."""
	def __init__(self, filename):
		self.filename = filename
		self.records = self.import_data()

	def import_data(self, verbose=False):
		if verbose: print self.field_names()
		return N.loadtxt(self.filename, comments='"', dtype=self.create_dtype())

	def field_names(self):
		with open(self.filename, "r") as f:
			field_names = f.readline()
			field_names = ' '.join(field_names.split()).replace('" "', ',').replace('"',"")
			field_names = field_names.split(",")
		return field_names

	def create_dtype(self):
		return [(n,float) for n in self.field_names()]

	def transform_coordinates(self, seed_file):
		dtype = [("point", int), ("x", float), ("y", float)]
		try:
			affine_seed = N.loadtxt(seed_file, comments="#", dtype=dtype)
		except IOError:
			print "No affine seed points available for "+seed_file
			return self.records

		fromCoords = []
		toCoords = []
		for a in affine_seed:
			idx = self.records['Line Numbers'] == a['point']
			point = self.records[idx][0]
			cord = [point[i+" Stage Coordinates (mm)"] for i in ["X","Y"]]
			tocord = [a["x"], a["y"]]
			print u"{} -> {}".format(repr(cord),repr(tocord))
			fromCoords.append(cord)
			toCoords.append(tocord)

		affine = Affine.construct(fromCoords, toCoords, verbose=True)

		incoords = [self.records[i+" Stage Coordinates (mm)"] for i in ["X","Y"]]
		incoords = N.transpose(N.vstack(incoords))
		outcords = affine.transform(incoords)
		for i,a in enumerate(["X","Y"]):
			self.records[a+" Stage Coordinates (mm)"] = outcords[:,i]

	def row(self, id):
		idx = self.records['Line Numbers'] == id
		return ArrayRow(self.records[idx][0])

	def each(self,id_list=None):
		for row in self.records:
			yield ArrayRow(row)

class ArrayRow(object):
	def __init__(self,row):
		self.data = row
		self.id = int(row["Line Numbers"])

	def get(self,name):
		return self.data[name]

	@property
	def geometry(self):
		coords = [self.data[a+" Stage Coordinates (mm)"] for a in "X Y".split()]
		return Point(*coords)

	def oxide_weights(self):
		oxides = {"Total": self.data["Oxide Totals"]}
		for oxide in app.config.get("OXIDES"):
			oxides[oxide] = self.data[oxide+" Oxide Percents"]
		return oxides

	def errors(self):
		errors = {}
		for cation in app.config.get("CATIONS"):
			errors[cation] = self.data[cation+" Percent Errors"]
		return errors