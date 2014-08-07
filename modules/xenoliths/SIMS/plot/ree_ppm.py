#!/usr/bin/env python
# coding=utf-8

from __future__ import division

import os
import json
import IPython

import periodictable as pt
import matplotlib.pyplot as P
import numpy as N

from uncertainties import ufloat

colors = {
	"CK-2": "#456AA0",
	"CK-3": "#FF9700",
	"CK-4": "#FFD100",
	"CK-5": "#3A9B88",
	"CK-6": "#FF2C00",
	"CK-7": "#8BD750"
}

data_dir = "raw"
plot_dir = "plots"

def elements():
	return sorted(pt.elements, key=lambda x: x.number)	

def load(file):
	dtype = [("el", str, 2), ("abundance", float), ("err", float)]
	return N.loadtxt(file, skiprows=2, dtype=dtype)

def build_series(file):
	data = load(f)
	x = [getattr(pt,i["el"]).number for i in data]
	y = [ufloat(i["abundance"],i["err"]) for i in data]
	return x,y

def setup_axis(ax, limits=None, type="nrm"):
	ax.set_yscale('log')

	ax.xaxis.set_ticks(ticks)
	ax.xaxis.set_ticklabels(labels)

	if limits is not None:
		ax.set_ylim(limits)
	ax.set_xlim([pt.La.number-0.5,pt.Lu.number+0.5])

	if type == "ppm":
		lbl = "CPX abundance (ppm)"
	if type == "nrm":
		lbl = "CPX / CI chondrite"
	ax.set_ylabel(lbl)	


with open("index.json", "r") as f:
	index = json.load(f)

elements = elements()
ticks = [el.number for el in elements]
labels = [el.symbol for el in elements]
labels[pt.promethium.number] = "--"

for typ in ["ppm","nrm"]:
	if typ == "ppm":
		limits = [1e-1,1e1]
	else:
		limits = [1e-1,1e2]

	fig_all = P.figure()
	ax_all = fig_all.add_subplot(111)

	fig_allavg = P.figure()
	ax_allavg = fig_allavg.add_subplot(111)

	fig_avg = P.figure()
	ax_avg = fig_avg.add_subplot(111)

	## Normalized ##
	for sample, files in index.iteritems():
		files = [os.path.join(os.path.dirname(__file__),data_dir, f+".asc."+typ) for f in files]
		print sample

		fig = P.figure()
		ax = fig.add_subplot(111)
		series = []
		for f in files:
			try:
				x,data = build_series(f)
			except IOError, err:
				print "File {} does not exist".format(f)
				continue
			series.append(data)
			x = x[4:-1]
			s = N.array([i.s for i in data[4:-1]])
			y = N.array([i.n for i in data[4:-1]])
			bottom = y-s
			bottom[bottom < 0] = .1 * y[bottom < 0]
	  
			ax.fill_between(x, bottom, y+s, facecolor="#666666", edgecolor="none", alpha=0.2)
			ax.plot(x,y, color="k")

			ax_allavg.plot(x,y, color=colors[sample], alpha=0.6, linewidth=0.5)
			ax_allavg.fill_between(x, bottom, y+s, facecolor=colors[sample], edgecolor="none", alpha=0.1)
 
			ax_all.plot(x,y, color=colors[sample], linewidth=1  )
			ax_all.fill_between(x, bottom, y+s, facecolor=colors[sample], edgecolor="none", alpha=0.2)

		## averaged
		data = [sum(i)/len(series) for i in zip(*tuple(series))]
		s = N.array([i.s for i in data[4:-1]])
		y = N.array([i.n for i in data[4:-1]])
		bottom = y-s
		bottom[bottom < 0] = .1 * y[bottom < 0]
		ax_avg.plot(x,y, color=colors[sample], linewidth=2)
		ax_allavg.plot(x,y, color=colors[sample], linewidth=2)

		ax_avg.fill_between(x, y-s, y+s, facecolor=colors[sample], edgecolor="none", alpha=0.2)


		setup_axis(ax, limits, typ)
		fig.savefig("plots/{0}.{1}.pdf".format(sample, typ), bbox_inches="tight")

	setup_axis(ax_all, limits, typ)
	fig_all.savefig("plots/all.{0}.pdf".format(typ), bbox_inches="tight")

	setup_axis(ax_avg, limits, typ)
	fig_avg.savefig("plots/all_avg.{0}.pdf".format(typ), bbox_inches="tight")

	setup_axis(ax_allavg, limits, typ)
	fig_allavg.savefig("plots/all_allavg.{0}.pdf".format(typ), bbox_inches="tight")

IPython.embed()