#!/usr/bin/env python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import uncertainties
from django.conf import settings
from samples.models import Point
import IPython
import numpy as N

opx = Point.objects.get(uid="CK-4_810")
cpx = Point.objects.get(uid="CK-4_986")

class Thermometer(object):
	def __init__(self,opx, cpx, pressure=1.5):
		self.formula = {
			"opx": opx.compute_formula(6),
			"cpx": cpx.compute_formula(6)
		}
		self.P = pressure #GPa

class BKN(Thermometer):
	def __init__(self, *args, **kwargs):
		super(Thermometer, self).__init__(self,*args,**kwargs)

	def temperature(self):
		23664+(24.9+126.3)

class Taylor1998(Thermometer):
	def __init__(self, *args, **kwargs):
		super(Thermometer, self).__init__(self,*args,**kwargs)

	def Al_octahedral(self, type):
		f = self.formula[type]
		return f["Al"]/2-f["Cr"]/2-f["Ti"]+f["Na"]/2

	def Al_tetrahedral(self, type):
		f = self.formula[type]
		return f["Al"]/2+f["Cr"]/2+f["Ti"]-f["Na"]/2

	def X_ts(self):
		"""
		A correction for tschermak substitution 
		(3+ cation in both octahedral and tetrahedral site
		"""
		f = self.formula["cpx"]
		return f["Al"]+f["Cr"]-f["Na"]

	def a_en(self, type):
		"A term for the activity of enstatite"
		f = self.formula[type]
		a = 1-f["Ca"]-f["Na"]
		b = 1-self.Al_octahedral(type)-f["Cr"]-f["Ti"]
		c = (1-self.Al_tetrahedral(type)/2)**2
		activity = a*b*c
		return activity


	def temperature(self):
		cpx = self.formula["cpx"]
		opx = self.formula["opx"]

		lnKd = N.log(self.a_en("cpx"))-N.log(self.a_en("opx"))

		bottom = sum([
			15.67,
			14.37*cpx["Ti"],
			3.69*cpx["Fe"],
			-3.25*self.X_tschermak(),
			lnKd**2
		])
		print bottom

		T = (24787+678*self.P)/bottom
		IPython.embed()
		return T

thermometer = Taylor1998(opx,cpx)
T = thermometer.temperature()
IPython.embed()

