"""Converts between coordinate systems. These can be compositional or literally anything."""
from ..config import OXIDES, MINERAL_SYSTEMS
import numpy as N

class SimpleConverter(object):
	def __init__(self, array, components, system="pyroxene"):
		self.system = system
		self.array = array
		self.components = components

	def transform(self, molar_percent):
		points = N.array([molar_percent.get(i,0) for i in OXIDES]).T
		result = N.dot(self.array,points)
		result = result/result.sum()
		return dict(zip(self.components,result))

	@classmethod
	def construct(cls, system="pyroxene"):
		system = MINERAL_SYSTEMS[system]
		ls = []
		components = []
		for i,component in system.iteritems():
			ls.append([component.get(j,0) for j in OXIDES])
			components.append(i)
		model = N.linalg.pinv(N.array(ls).T)
		return cls(model, components, system=system)


class Converter(object):
	def __init__(self, system="pyroxene"):
		system = MINERAL_SYSTEMS[system]
		self.in_components = [i for i in OXIDES]
		self.out_components = []
		array = []
		for name,component in system.iteritems():
			for key in component.keys():
				if not key in self.in_components:
					self.in_components.append(key)
		for name,component in system.iteritems():
			ls = [component.get(j,0) for j in self.in_components]
			array.append(ls)
			self.out_components.append(name)
		self.array = N.linalg.pinv(N.array(array).T)


	def preprocess(self, molar_data):
		out = []
		for name in self.in_components:
			if name not in OXIDES:
				# check for cases in which we are adding oxides
				items = name.split()
				for i, item in enumerate(items):
					if item in OXIDES:
						items[i] = "{0:.8g}".format(molar_data.get(item,0))
				expr = "".join(items)
				res = eval(expr)
			else:
				res = molar_data.get(name,0)
			out.append(res)
		return out

	def transform(self, molar_data):
		points = N.array(self.preprocess(molar_data)).T
		result = N.dot(self.array,points)
		result = result/result.sum()
		return dict(zip(self.out_components,result))
