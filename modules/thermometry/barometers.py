from __future__ import division
from uncertainties import ufloat
from uncertainties.umath import log
from django.conf import settings
from samples.group import get_cations
from .thermometers import Taylor1998

class Ca_Olivine(object):
	"""From Kohler and Brey, 1990"""
	name = "Ca in Olivine"
	def __init__(self, ol, cpx, uncertainties=True, breakout_errors=False):
		self.breakout_errors = breakout_errors

		self.cpx = get_cations(cpx, 6, uncertainties)
		self.ol = get_cations(ol, 4, uncertainties)

		self.D_Ca = self.ol["Ca"]/self.cpx["Ca"]

	def low_temperature(self, T):
		"""Need to implement the high temperature version if we are planning
		to measure rocks above ~1275C
		"""
		ans = -T*log(self.D_Ca)-5792-1.25*T
		return ans/42.5

	def pressure(self, T):
		return -self.low_temperature(T)/10
