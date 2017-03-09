#!/usr/bin/env python
# -- coding: utf-8 --

import json
import numpy as N
from project_options import colors

from samples.geotherm import HeatFlowModel
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

with open("separated.json", "r") as f:
	results = json.load(f)

fig = P.figure(figsize=(5,8))
ax = fig.add_subplot(111)
for t in results["multiple"]:
	ax.scatter(t["T_ta98"], t["heatflow"]["z"], marker="o", s=12, alpha=0.4, color="#cccccc", zorder=-10)
	ax.scatter(t["T_ta98"], t["olivine"]["z"], marker="o", s=35, alpha=0.4, color=colors[t["sample"]])
ax.invert_yaxis()
ax.set_xlabel("Temperature - TA98 (\u00b0C)")
ax.set_ylabel("Depth (km)")
#ax.set_xlim([940,1150])
ax.set_xlim([800,1200])
ax.set_ylim([130,40])
ax.set_xticks([800,900,1000,1100,1200])
ax.set_yticks([40,60,80,100,120])
#ax.set_ylim([120,0])
ax.autoscale(False)
y = N.linspace(0,150,150)
m = HeatFlowModel(q_0=90)
T = N.array(list(map(m.temperature, y)))
ax.plot(T,y,color="#cccccc", zorder=-20)

fig.savefig("output/geotherm.pdf", bbox_inches="tight")

