#!/usr/bin/env python
# -- coding: utf-8 --

import json
import numpy as N
#from project_options import colors
import IPython
import matplotlib as M
import matplotlib.pyplot as P
import pandas

colors = {
	"CK-2": "#456AA0",
	"CK-3": "#FF9700",
	"CK-4": "#FFD100",
	"CK-5": "#3A9B88",
	"CK-6": "#FF2C00",
	"CK-7": "#8BD750"
}

with open("results.json", "r") as f:
	results = json.load(f)

def comparator(x):
	"""Sorts data in ascending order"""
	return N.array(x["core"]["ta98"]["separate"]["values"]).mean()

results.sort(key=comparator)



#df = pandas.DataFrame(data, columns=columns)

fig = P.figure()
ax = fig.add_subplot(111)

data = []
columns = []
color = []
widths = []
for sample in results:
	columns.append(sample["id"])
	data.append(sample["rim"]["ta98"]["separate"]["values"])
	color.append(colors[sample["id"]])
	width = 30
	widths += [width,width/4]

rim = S.violin(
	data,
	names=columns,
	inner='points',
	ax=ax,
	alpha=0.2,
	color=color,
	widths=0.3
)

[l.set_linewidth(0.1) for l in rim.lines]

data = []
for sample in results:
	data.append(sample["core"]["ta98"]["separate"]["values"])
	#color += [colors[sample["id"]]]*2
	#width = 30
	#widths += [width,width/4]

core = S.violin(
	data,
	inner='points',
	ax=ax,
	color=color,
	alpha=0.9,
	#widths=0.9
)



fig.savefig("output/violin.pdf", bbox_inches="tight")

