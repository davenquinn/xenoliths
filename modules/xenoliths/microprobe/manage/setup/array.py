import numpy as N
import json
import os

from pandas import read_table
from shapely.geometry import Point
from ....application import app

class Array(object):
	"""A wrapper around a .dat file obtained for the electron microprobe."""
	def __init__(self, filename):
		self.filename = filename
		self.frame = read_table(filename)

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
