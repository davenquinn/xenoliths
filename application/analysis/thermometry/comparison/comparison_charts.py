#!/usr/bin/env python
from __future__ import division
import os

import matplotlib.pyplot as P
import numpy as N
import json
import IPython
from project_options import colors

directory = os.path.dirname(os.path.abspath( __file__ ))
path = os.path.join(directory, "..","separated","results_opx.json")
with open(path, "r") as f:
	data = json.load(f)

thermometers = [
	{"id":"ta98","name": "TA98"},
	{"id":"bkn", "name": r"T$_{BKN}$"},
	{"id": "ca_opx", "name": "Ca-in-Opx"},
	{"id": "ca_opx_corr", "name": "Ca-in-OPX (Nimis and Grutter, 2010 correction)"}
	]


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

def plot_grouped(th1,th2):
	names = [th["name"] for th in [th1,th2]]
	ids = [th["id"] for th in [th1,th2]]
	print ids
	fig = P.figure()
	ax = fig.add_subplot(111)

	for sample in data:
		name = sample["id"]
		x = []
		y = []
		for a_loc in ["core", "rim"]: 
			values = [sample[a_loc][i]["grouped"]["val"] for i in ids]
			ax.scatter(values[0],values[1],zorder=10, marker="o", **props[a_loc])
			x.append(values[0])
			y.append(values[1])
		ax.plot(x,y,color="#888888")
		ax.annotate(name, xy=(sum(x)/2, sum(y)/2), **annotate_props)

	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles[0:2],labels[0:2],scatterpoints=1,loc="best")

	ax.set_xlim([960,1120])
	ax.set_ylim([960,1120])
	ax.autoscale(False)
	ax.plot([0,1800],[0,1800],color="#cccccc", zorder=-20)
	ax.set_xlabel(u"{0} \u00b0C".format(names[0]))
	ax.set_ylabel(u"{0} \u00b0C".format(names[1]))

	fig.suptitle("{0} vs. {1} (Grouped, P = {2:.1f} GPa)".format(names[1], names[0],1.5))
	path = os.path.join(directory, "output", "{0}-{1}.grouped.pdf".format(ids[1], ids[0]))
	fig.savefig(path, bbox_inches="tight")

def plot_separated(th1,th2):
	names = [th["name"] for th in [th1,th2]]
	ids = [th["id"] for th in [th1,th2]]
	print ids
	fig = P.figure()
	ax = fig.add_subplot(111)

	for sample in data:
		name = sample["id"]
		
		for a_loc in ["core", "rim"]: 
			values = [sample[a_loc][i]["separate"]["values"] for i in ids]		
			if a_loc == "core":
				popts = dict(color=colors[name])
			elif a_loc == "rim":
				popts = dict(edgecolor=colors[name], color="#ffffff")
			ax.scatter(values[0], values[1], marker="o", s=20, alpha=0.7, **popts)


	ax.set_xlim([900,1150])
	ax.set_ylim([900,1150])
	ax.set_xlabel(u"{0} \u00b0C".format(names[0]))
	ax.set_ylabel(u"{0} \u00b0C".format(names[1]))
	ax.autoscale(False)
	ax.plot([0,1800],[0,1800],color="#cccccc", zorder=-20)


	fig.suptitle("{0} vs. {1} (Separated, P = {2:.1f} GPa)".format(names[1], names[0],1.5))
	path = os.path.join(directory, "output", "{0}-{1}.separate.pdf".format(ids[1], ids[0]))
	fig.savefig(path, bbox_inches="tight")


for th1 in thermometers:
	for th2 in thermometers:
		if th1 == th2: continue
		plot_grouped(th1,th2)
		plot_separated(th1,th2)




