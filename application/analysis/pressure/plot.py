#!/usr/bin/env python
# -- coding: utf-8 --

import json
import matplotlib.pyplot as P
import numpy as N
from project_options import colors

from samples.geotherm import HeatFlowModel

with open("separated.json", "r") as f:
	results = json.load(f)

for meas in ["single", "multiple"]:
	fig = P.figure()
	ax = fig.add_subplot(111)
	for t in results[meas]:
		ax.scatter(t["T_ta98"], t["olivine"]["z"], marker="o", s=22, alpha=0.6, color=colors[t["sample"]])
	ax.invert_yaxis()
	ax.set_xlabel(u"Temperature - TA98 (\u00b0C)")
	ax.set_ylabel(u"Depth (km)")
	#ax.set_xlim([400,1100])
	#ax.set_ylim([100,40])
	ax.autoscale(False)
	y = N.linspace(0,150,150)
	m = HeatFlowModel(q_0=90)
	T = N.array(map(m.temperature, y))
	ax.plot(T,y,color="#cccccc", zorder=-20)
	fig.savefig("output/{0}.pdf".format(meas), bbox_inches="tight")

	fig = P.figure()
	ax = fig.add_subplot(111)
	for t in results[meas]:
		ax.scatter(t["T_ta98"], t["heatflow"]["z"], marker="o", s=22, alpha=0.6, color=colors[t["sample"]])
	ax.invert_yaxis()
	ax.set_xlabel(u"Temperature - TA98 (\u00b0C)")
	ax.set_ylabel(u"Depth (km)")
	ax.set_xlim([930,1100])
	ax.set_ylim([58,46])
	ax.autoscale(False)
	y = N.linspace(0,150,150)
	m = HeatFlowModel(q_0=90)
	T = N.array(map(m.temperature, y))
	ax.plot(T,y,color="#cccccc", zorder=-20)
	fig.savefig("output/{0}_geotherm.pdf".format(meas), bbox_inches="tight")


	figa = P.figure()
	ax = figa.add_subplot(111)
	for t in results[meas]:
		ax.scatter(t["heatflow"]["z"], t["olivine"]["z"], marker="o", s=22, alpha=0.6, color=colors[t["sample"]])
	ax.set_xlabel(u"Depth (km) - "+r"90 mW/m^$2$ geotherm")
	ax.set_ylabel(u"Depth (km) - Ca-in-olivine geobarometer")
	#ax.set_xlim([40,140])
	#ax.set_ylim([40,140])
	ax.autoscale(False)
	ax.plot([0,1800],[0,1800],color="#cccccc", zorder=-20)
	figa.savefig("output/{0}_comparison.pdf".format(meas), bbox_inches="tight")	


