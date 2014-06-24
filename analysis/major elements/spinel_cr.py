#!/usr/bin/env python
# -- coding: utf-8 --

from __future__ import division
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.contrib.gis.geos import *

import json
import numpy as N
import IPython

from uncertainties import ufloat
from django.conf import settings

from samples.models import Sample, Point

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

fig = P.figure(figsize=(5,8))
ax = fig.add_subplot(111)

base_queryset = Point.objects.remove_bad()

for i,sample in enumerate(Sample.objects.all()):


	sample_queryset = base_queryset.filter(sample=sample)
	print ""
	print sample.id

	sp = sample_queryset.filter(mineral="sp").distinct()
	for s in sp:
		cations = s.oxides
		ax.scatter(cations["Al2O3"],cations["Cr2O3"], marker="o", s=35, alpha=0.6, color=colors[sample.id])

ax.set_xlabel(r"Al$_\textrm{2}$O$_\textrm{3}$ (%wt)")
ax.set_ylabel(r"Cr$_\textrm{2}$O$_\textrm{3}$ (%wt)")

fig.savefig("spinel_cr.pdf", bbox_inches="tight")





