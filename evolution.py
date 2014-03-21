#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
Usage: evolution.py [--progressive]

Options:
--progessive  Print progressive time slices
"""

from __future__ import division
import numpy as N
from docopt import docopt
import IPython
from matplotlib import pyplot as P
from heat_flow.oceanic import GDH_Model
import time

args = docopt(__doc__)

oceanic_crust = GDH_Model()

depth = N.linspace(0,95,950)


fig = P.figure()
ax = fig.add_subplot(111)
ax.set_ylim([95,0])
ax.set_xlim([0,1600])
fig.show()
T = oceanic_crust.temperature(depth,1, order=1500)
line, = ax.plot(T, depth)
fig.canvas.draw()


if args["--progressive"]:
	for i in range(500):
		T = oceanic_crust.temperature(depth,i+1)
		line.set_xdata(T)
		time.sleep(0.05)
		fig.canvas.draw()

IPython.embed()
