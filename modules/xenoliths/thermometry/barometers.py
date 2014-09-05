from __future__ import division
from uncertainties import ufloat
from uncertainties.umath import log
from ..microprobe.group import get_cations

class Ca_Olivine(object):
	"""From Kohler and Brey, 1990"""
	name = "Ca in Olivine"
	def __init__(self, ol, cpx, **kwargs):
		self.breakout_errors = kwargs.pop("breakout_errors",False)

		self.cpx = get_cations(cpx, oxygen=6, **kwargs)
		self.ol = get_cations(ol, oxygen=4, **kwargs)

		self.D_Ca = self.ol["Ca"]/self.cpx["Ca"]

	def low_temperature(self, T):
		"""Need to implement the high temperature version if we are planning
		to measure rocks above ~1275C
		"""
		ans = -T*log(self.D_Ca)-5792-1.25*T
		return ans/42.5

	def pressure(self, T):
		return -self.low_temperature(T)/10
