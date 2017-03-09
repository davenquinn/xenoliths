#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import IPython
import json
import matplotlib.pyplot as P
import numpy as N
from samples.thermometry.geotherm import HeatFlowModel
from project_options import colors

directory = os.path.dirname(os.path.abspath( __file__ ))
path = os.path.join(directory, "..","thermometry", "errors", "data.json")
with open(path, "r") as f:
	data = json.load(f)

annotate_props = dict(xytext=(5,-5), textcoords='offset points', ha='left', va='center')

m = HeatFlowModel(q_0=90)

y = N.linspace(0,60,100)
T = N.array(list(map(m.temperature, y)))

fig = P.figure()
ax = fig.add_subplot(111)
ax.plot(T,y,color="#222222", zorder=-10)

for sample in data["samples"]:
	temp = sample["core"]["T"]
	d = m.get_depth(temp)[0]
	ax.scatter(temp,d, marker="o", s=35, alpha=0.6, color=colors[sample["id"]])
	#ax.annotate(sample["id"], xy=(temp, d), **annotate_props)
	
ax.set_xlabel("Temperature \u00b0C ")
ax.set_ylabel("Depth (m)") 
ax.invert_yaxis()
ax.set_ylim([60,0])
ax.set_xlim([0,1200])

fig.suptitle('Core temperatures (assuming 1.5 GPa) "pinned"\nto a 90 W/m$^2$ steady state geotherm')
path = os.path.join(directory, "output", "heat_flow.pdf")
fig.savefig(path)

ax.set_ylim([60,45])
ax.set_xlim([900,1100])
path = os.path.join(directory, "output", "heat_flow_zoom.pdf")
fig.savefig(path)

