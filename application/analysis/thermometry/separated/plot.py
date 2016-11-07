#!/usr/bin/env python
# -- coding: utf-8 --

import json
import matplotlib.pyplot as P
import brewer2mpl
import IPython
import numpy as N
from project_options import colors

with open("results.json", "r") as f:
	results = json.load(f)

def comparator(x):
	"""Sorts data in ascending order"""
	return N.array(x["core"]["ta98"]["separate"]["values"]).mean()

results.sort(comparator)


thermometers = {
	"bkn": "BKN",
	"ca_opx": "Ca-OPX",
	"ta98": "TA98"
}

fig = P.figure()
ax = fig.add_subplot(111)
for s in results:
	for typeid in ["core","rim"]:
		t = s[typeid][thermometer]
		if typeid == "core":
			popts = dict(color=colors[s["id"]])
		elif typeid == "rim":
			popts = dict(edgecolor=colors[s["id"]], color="none")
		for val in t["separate"]["values"]:
			ax.scatter(t["grouped"]["val"], val, marker="o", s=22, alpha=0.6, **popts)

	string = r"T$_{"+tname+r"}$ ($^{\circ}$C)"
	ax.set_xlabel(string + " - Grouped per-sample")
	ax.set_ylabel(string + " - Individual pairs")
	ax.autoscale(False)
	ax.plot([0,1800],[0,1800],color="#cccccc", zorder=-20)

	fig.savefig("output/{0}.pdf".format(thermometer), bbox_inches="tight")


# fig, axes = P.subplots(nrows=6, ncols=1, sharex=True, sharey=True)
# fig.tight_layout()

# samples = ["CK-"+str(i) for i in range(2,8)]
# bins = N.arange(920,1100, 5)

# for ax, sample in zip(axes, samples):
# 	s = next((x for x in results if x["id"] == sample), None)
# 	for typeid in ["core","rim"]:
# 		if typeid == "core":
# 			popts = dict(facecolor=colors[s["id"]])
# 		elif typeid == "rim":
# 			popts = dict(edgecolor="k", facecolor="none")
# 		t = s[typeid]
# 		n, bins, patches = ax.hist(t["separate"]["values"], bins, normed=False, histtype='stepfilled', **popts)

# fig.subplots_adjust(hspace=0)
# P.setp([a.get_xticklabels() for a in axes[:-1]], visible=False)
# fig.savefig("output/histogram.pdf")


