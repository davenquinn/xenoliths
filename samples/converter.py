"""Converts between coordinate systems. These can be compositional or literally anything."""
from django.conf import settings
import numpy as N

class Converter(object):
	def __init__(self, array, components):
		self.array = array
		self.components = components

	def transform(self, molar_percent):
		points = N.array([molar_percent.get(i,0) for i in settings.OXIDES]).T
		result = N.dot(self.array,points)
		result = result/result.sum()
		return dict(zip(self.components,result))

	@classmethod
	def construct(cls, system="pyroxene"):
		system = settings.MINERAL_SYSTEMS[system]
		ls = []
		components = []
		for i,component in system.iteritems():
			ls.append([component.get(j,0) for j in settings.OXIDES])
			components.append(i)
		model = N.linalg.pinv(N.array(ls).T)
		return cls(model, components)