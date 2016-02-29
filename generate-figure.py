#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import IPython

import numpy as N
import matplotlib as M
M.use("pgf")

from matplotlib import pyplot as P

pgf_with_pdflatex = {
    "pgf.rcfonts": False,
    "pgf.preamble": [
    	r"\usetypescript[helvetica][uc]",
		r"\setupbodyfont[helvetica]",
         r"\usepackage{fontspec,xunicode,xltxtra,siunitx,mhchem}",
         r"\setmainfont{Helvetica Neue}"
    ]
}
M.rcParams.update(pgf_with_pdflatex)

names = [("Names", "S4")]+[(i, float) for i in "Sr_ratio Nd_ratio E_nd".split()]

data = N.loadtxt("isotope-data.tsv",comments="#",dtype=names)

fig = P.figure()
ax = fig.add_subplot(111)
ax.plot(data["Sr_ratio"],data["E_nd"], "ko")

ax.set_xlabel(r"$^\textrm{87}$Sr/$^\textrm {86}$Sr$")
ax.set_ylabel(r"$\mathcal{E}_\ce{Nd}$")
ax.set_ylim([-5,12])
ax.set_xlim([0.7015,0.708])
ax.annotate("Crystal Knob", xy=(data["Sr_ratio"].mean(),data["E_nd"].mean()), xycoords="data", textcoords="offset points", xytext=(15,-4))

ax.axhline(y=0, color="#999999", linestyle="dotted")
ax.axvline(x=.7045, color="#999999", linestyle="dotted")

#ax.plot(.7045,0, color="none", markeredgecolor="#999999", marker="o", markersize=10)

# Bulk earth from DePaolo and Wasserburg, 1976
ax.annotate("Bulk Earth", xy=(.7045,0), xycoords="data", textcoords="offset points", xytext=(5,5))

fig.suptitle("Paired Sm-Nd and Rb-Sr isotopes", fontsize=18)
fig.savefig("isotopes.pdf", bbox_inches="tight")

