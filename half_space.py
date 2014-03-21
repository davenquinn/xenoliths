"""
This is an implementation of the half-space cooling model for the oceanic lithosphere
discussed in Turcotte and Schubert, Geodynamics, 2002 (p287).
"""
from __future__ import division
from scipy.special import erf,erfc, erfcinv
import numpy as N
from pint import UnitRegistry
u = UnitRegistry()
Q_ = u.Quantity

def set_unit(q,default):
	"""Applies the default unit if no unit is applied"""
	try:
		return q.to(default)
	except AttributeError:
		return q * default

class BaseModel(object):
	defaults = {}
	def __init__(self,**kwargs):
		for key,item in self.defaults.items():
			i = Q_(kwargs.get(key,item[0]),item[1])
			setattr(self, key, i)


class MaterialModel(BaseModel):
	defaults = {
		"conductivity": (3.35,"W/m/K"),
		"specific_heat": (1171,"J/K/kg"),
		"density": (3000,"kg/m**3")
	}
	def __init__(self,**kwargs):
		super(MaterialModel, self).__init__(**kwargs)

	@property
	def diffusivity(self):
		a = self.conductivity/self.specific_heat/self.density
		return a.to("m**2/s")

	def length_scale(self, time):
		"""
		The distance over which heat will propagate in a given time period.
		Accepts time in seconds
		"""
		return N.sqrt(self.diffusivity*set_unit(time,u.second))

	def time_scale(self, distance=1000):
		"""
		The time over which temperature changes will propagate a given distance.
		Accepts distance in meters (default 1km)
		"""
		return (set_unit(distance,u.meter)**2/self.diffusivity)

class HalfSpace(BaseModel):
	defaults = {
		"T_surface": (25,"degC"),
		"T_max": (1500,"degC"),
		"T_lithosphere": (1300,"degC")
	}
	def __init__(self, material_model, **kwargs):
		super(HalfSpace, self).__init__(**kwargs)
		self.material = material_model

	def temperature(self,time,depth):
		time = set_unit(time, u.seconds)
		depth = set_unit(depth, u.meters)
		d = self.material.length_scale(time)
		t = erfc(float(depth/(2*d)))*(self.T_max-self.T_surface)+self.T_surface
		return t.to(u.degC)

	def depth(self,time,temperature):
		temp = set_unit(temperature, u.degC)
		theta = (temp-self.T_max).magnitude/(self.T_surface-self.T_max).magnitude
		eta = erfcinv(theta)
		return 2*eta*self.material.length_scale(time)

	def lithospheric_thickness(self,time):
		return self.depth(time,self.T_lithosphere)
