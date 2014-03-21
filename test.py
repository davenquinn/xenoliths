#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import IPython
from half_space import *
import matplotlib.pyplot as P
import seaborn as sns

m = MaterialModel()

space = HalfSpace(m)

def plot_halfspace():
	times = N.linspace(0, 1e8,100)*u.year
	series = range(1,8)
	with sns.palette_context("RdPu",len(series)):
		for i in series:
			T = i*200
			depths = N.array(space.depth(times,T))
			P.plot(times, depths/1000)
			ax = P.gca()
			ax.set_xlabel("Time (years)")
			ax.set_ylabel("Base of Lithosphere (km)")
			ax.invert_yaxis()
	P.show()


IPython.embed()
