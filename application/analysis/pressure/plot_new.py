#!/usr/bin/env python
# -- coding: utf-8 --

import json
import numpy as N
from project_options import colors

from samples.geotherm import HeatFlowModel
import matplotlib as M
#M.use("pgf")
import matplotlib.pyplot as P

"""pgf_with_pdflatex = {
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
M.rcParams.update(pgf_with_pdflatex)"""

with open("separated.json", "r") as f:
	results = json.load(f)

fig = P.figure(figsize=(5,8))
ax = fig.add_subplot(111)
for t in results["multiple"]:
	ax.scatter(t["T_ta98"], t["heatflow"]["z"], marker="o", s=10, alpha=0.4, color="#cccccc", zorder=-10)
	ax.scatter(t["T_ta98"], t["olivine"]["z"], marker="o", s=35, alpha=0.4, color=colors[t["sample"]])
ax.invert_yaxis()
ax.set_xlabel(u"Temperature - TA98 (\u00b0C)")
ax.set_ylabel(u"Depth (km)")
#ax.set_xlim([940,1150])
ax.set_xlim([850,1350])
ax.set_ylim([130,40])
#ax.set_ylim([120,0])
ax.autoscale(False)
y = N.linspace(0,150,150)
m = HeatFlowModel(q_0=90)
T = N.array(map(m.temperature, y))
ax.plot(T,y,color="#cccccc", zorder=-20)

context = fig.add_axes([0.62,0.13,0.25,0.53])
context.plot(T,y,color="#cccccc", zorder=-20)
context.invert_yaxis()
context.set_xlim([0,1300])
context.set_ylim([150,0])
context.set_yticks([0,50,100,150])
context.set_xticks([0,1000])
for t in results["multiple"]:
	context.scatter(t["T_ta98"], t["olivine"]["z"], marker="o", s=5, alpha=0.6, color=colors[t["sample"]])


fig.savefig("output/everything.pdf", bbox_inches="tight")

