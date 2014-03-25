#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import IPython
import numpy as N
import matplotlib.pyplot as P
import seaborn as sns

from geotherm.units import registry
from geotherm.models import HalfSpace, MaterialModel

m = MaterialModel()
half_space = HalfSpace(m)

def plot_halfspace():
	times = N.linspace(0, 1e8, 100)*registry.year
	series = range(1,8)
	with sns.palette_context("RdPu",len(series)):
		for i in series:
			T = i*200
			depths = N.array(half_space.depth(times,T))
			P.plot(times, depths/1000)
			ax = P.gca()
			ax.set_xlabel("Time (years)")
			ax.set_ylabel("Base of Lithosphere (km)")
			ax.invert_yaxis()
	P.show()


IPython.embed()
