#!/usr/bin/env python
from __future__ import division
import os

import matplotlib.pyplot as P
import numpy as N
import json
import IPython

directory = os.path.dirname(os.path.abspath( __file__ ))
path = os.path.join(directory, "data.json")
with open(path, "r") as f:
	data = json.load(f)

runs = {
	"ca_opx": {
		"label": "Ca-in-Opx"
	},
	"bkn": {
		"label": "BKN"
	}
}


props = {
	"core": {
		"label": "Core",
		"color": "black"
	},
	"rim": {
		"label": "Rim",
		"color": "#eeeeee",
		"edgecolor": "black"
	}
}
annotate_props = dict(xytext=(5,-5), textcoords='offset points', ha='left', va='center')

for key,item in runs.items():

	fig = P.figure()
	ax = fig.add_subplot(111)

	for name, sample in data["samples"].items():
		x = []
		y = []
		for a_loc, analysis in sample.items():
			ax.scatter(analysis["ta98"], analysis[key],zorder=10, marker="o", **props[a_loc])
			x.append(analysis["ta98"])
			y.append(analysis[key])
		ax.plot(x,y,color="#888888")
		ax.annotate(name, xy=(sum(x)/2, sum(y)/2), **annotate_props)

	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles[0:2],labels[0:2],scatterpoints=1,loc="best")

	ax.set_xlabel(u"TA98 \u00b0C ")
	ax.set_ylabel(u"{0} \u00b0C".format(item["label"]))

	fig.suptitle("{0} vs. TA98 (P = {1:.1f} GPa)".format(item["label"],data["config"]["pressure"]))
	path = os.path.join(directory, "output", "{0}_ta98.svg".format(key))
	fig.savefig(path)

