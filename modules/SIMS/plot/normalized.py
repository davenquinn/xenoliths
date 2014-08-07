from __future__ import division

import os
import json

import periodictable as pt
import matplotlib.pyplot as P
import numpy as N

from uncertainties import ufloat

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

with open("index.json", "r") as f:
	index = json.load(f)

elements = elements()
ticks = [el.number for el in elements]
labels = [el.symbol for el in elements]
labels[pt.promethium.number] = "--"

## Normalized ##
for sample, files in index.iteritems():
	files = [os.path.join(os.path.dirname(__file__),data_dir, f+".asc.nrm") for f in files]
	print sample

	fig = P.figure()
	ax = fig.add_subplot(111)
	for f in files:
		try:
			x,y = build_series(f)
		except IOError, err:
			print "File {} does not exist".format(f)
			continue
		x = x[4:-1]
		s = N.array([i.s for i in y[4:-1]])
		y = N.array([i.n for i in y[4:-1]])

		ax.fill_between(x, y-s, y+s, facecolor="#666666", edgecolor="none", alpha=0.5)
		ax.plot(x,y, color="k")
	ax.set_yscale('log')

	ax.xaxis.set_ticks(ticks)
	ax.xaxis.set_ticklabels(labels)

	ax.set_ylim([1e-1,1e2])
	ax.set_xlim([pt.La.number-0.5,pt.Lu.number+0.5])

	ax.set_ylabel("CPX / CI chondrite")
	fig.suptitle(sample+": clinopyroxene rare-earth elements")

	filename = "plots/{0}.norm.pdf".format(sample)
	fig.savefig(filename, bbox_inches="tight")

### All combined

colors = {
	"CK-2": "#A6CEE3",
	"CK-3": "#1F78B4",
	"CK-4": "#B2DF8A",
	"CK-5": "#33A02C",
	"CK-6": "#FB9A99",
	"CK-7": "#E31A1C"
}

fig = P.figure()
ax = fig.add_subplot(111)

for sample, files in index.iteritems():
	files = [os.path.join(os.path.dirname(__file__),data_dir, f+".asc.nrm") for f in files]
	print sample

	for f in files:
		try:
			x,y = build_series(f)
		except IOError, err:
			print "File {} does not exist".format(f)
			continue
		x = x[4:-1]
		s = N.array([i.s for i in y[4:-1]])
		y = N.array([i.n for i in y[4:-1]])

		ax.fill_between(x, y-s, y+s, facecolor=colors[sample], edgecolor="none", alpha=0.2)

		ax.plot(x,y, color=colors[sample], linewidth=1)

ax.set_yscale('log')

ax.xaxis.set_ticks(ticks)
ax.xaxis.set_ticklabels(labels)

ax.set_ylim([1e-1,1e2])
ax.set_xlim([pt.La.number-0.5,pt.Lu.number+0.5])

ax.set_ylabel("CPX / CI chondrite")
fig.suptitle("Clinopyroxene rare-earth elements")

filename = "plots/all.norm.pdf"
fig.savefig(filename, bbox_inches="tight")


IPython.embed()
