#!/usr/bin/env python
# -- coding: utf-8 --

import json
import numpy as N
from project_options import colors
import IPython
import matplotlib as M
M.use("pgf")
import matplotlib.pyplot as P

pgf_with_pdflatex = {
	"pgf.texsystem": "xelatex",
	"pgf.rcfonts": True,
	"pgf.preamble": [
		r"\usepackage{fontspec}",
		r"\usepackage{siunitx}",
		r"\newfontfamily\bodyfont[]{Helvetica Neue Light}",
		#r"\RequirePackage[math-style=TeX,vargreek-shape=unicode]{unicode-math}",
		#r"\defaultfontfeatures{Mapping=tex-text}",
		r"\setmainfont{Helvetica Neue Light}"
	]
}

pgf_with_pdflatex = {
	"font.family": "sans-serif",
    "font.serif": [],                   # use latex default serif font
    "font.sans-serif": ["Helvetica"],
}
M.rcParams.update(pgf_with_pdflatex)

with open("results.json", "r") as f:
	results = json.load(f)

def comparator(x):
	"""Sorts data in ascending order"""
	return N.array(x["core"]["ta98"]["separate"]["values"]).mean()

results.sort(key=comparator)

fig = P.figure()
ax = fig.add_subplot(111)

converter = M.colors.colorConverter

for i,s in enumerate(results):
	print s["id"]
	color = colors[s["id"]]
	edgecolor = converter.to_rgba(color,.25)
	transcolor = converter.to_rgba(color,.2)
	popts = {
		"core": dict(s=50*4),
		"rim": dict(s=50)
	}
	for tname, opts in popts.items():
		data = s[tname]["ta98"]["separate"]["values"]
		if tname == "rim":
			a = i+.1
		else: 
			a = i-.1
		ax.scatter([a]*len(data),data, marker="o", color=transcolor,**opts)
		#ax.scatter([a]*len(data),data, marker="o", facecolors="none",edgecolors=edgecolor,**opts)
ax.set_xlim([-0.5,5.5])
ax.xaxis.set_ticklabels([""]+[s["id"] for s in results])
ax.yaxis.grid(color="#eeeeee", linestyle="solid", linewidth=1.5)
ax.set_ylabel(r"Temperature (\textdegree{}C)")
ax.set_axisbelow(True)
for tick in ax.xaxis.get_major_ticks():
	tick.label.set_fontsize(14)
	tick.tick1On = False 
	tick.tick2On = False 


for tick in ax.yaxis.get_major_ticks():
	tick.tick1On = False 
	tick.tick2On = False 

s = [0]
line1 = M.lines.Line2D(s,s, color="white", marker='o', markerfacecolor="#000000", markersize=(50*4)**.5, alpha=.2)
line2 = M.lines.Line2D(s,s, color="white", marker='o',markerfacecolor="#000000", markersize=50**.5, alpha=.2)
ax.legend((line1,line2),('Core','Rim'),numpoints=1, loc="upper left")

fig.savefig("output/test.pdf", bbox_inches="tight")

