#!/usr/bin/env python
from __future__ import division
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.conf import settings
import IPython
from uncertainties import ufloat
from samples.models import Sample
from samples.query import Group
from samples.thermometry import BKN, Taylor1998, Ca_OPX_Corr, aggregate_errors

import matplotlib.pyplot as P
import numpy as N

def header(text):
	print text
	print "="*len(text)

bkn_res = []
ta98_res = []
ca_px_res = []
samples = []
for sample in Sample.objects.all():
	opx = Group(sample=sample, mineral="opx", bad=False)
	cpx = Group(sample=sample, mineral="cpx", bad=False)
	opx_ions = opx.get_cations()
	cpx_ions = cpx.get_cations()
	header(sample.id)
	samples.append(sample.id)
	print "{0:3}|{1:18}|{2:18}".format("Ion", "Orthopyroxene", "Clinopyroxene")
	for item in settings.CATIONS:
		print u"{0:3}| {1:8.6fP}| {2:8.6fP}".format(item, opx_ions[item], cpx_ions[item])
	print ""

	for system,results in zip([BKN,Taylor1998,Ca_OPX_Corr],[bkn_res,ta98_res,ca_px_res]):
		thermometer = system(opx,cpx)
		name = thermometer.name
		T = thermometer.temperature(pressure=ufloat(1.5,.2,"pressure"))
		errors = aggregate_errors(T)
		print u" \n## {1}: {0:.2fP}\n".format(T,name)
		for (tag, error) in errors.items():
			print u"- {0}: {1:.2f}".format(tag, error)
		results.append(T.nominal_value)

	print ""

fig = P.figure()
ax = fig.add_subplot(111)
ax.plot(ta98_res,bkn_res, "ko", label="BKN")
ax.set_xlabel(u"TA98 \u00b0C ")
ax.set_ylabel(u"BKN \u00b0C")

props = dict(xytext=(5,-5), textcoords='offset points', ha='left', va='center')
for x,y,name in zip(ta98_res,bkn_res,samples):
	ax.annotate(name, xy=(x, y), **props)

fig.suptitle("BKN vs. TA98 (P = 1.5 GPa)")
outpath = os.path.join(settings.SITE_DIR,"scripts/output/thermometry/bkn_vs_ta98.pdf")
fig.savefig(outpath)

fig = P.figure()
ax = fig.add_subplot(111)
ax.plot(ta98_res,ca_px_res, "ko", label="Ca-in-Opx")
ax.set_xlabel(u"TA98 \u00b0C ")
ax.set_ylabel(u"Ca-in-Opx \u00b0C")

props = dict(xytext=(5,-5), textcoords='offset points', ha='left', va='center')
for x,y,name in zip(ta98_res,ca_px_res,samples):
	ax.annotate(name, xy=(x, y), **props)

fig.suptitle("Ca-in-OPx (corr) vs. TA98 (P = 1.5 GPa)")
outpath = os.path.join(settings.SITE_DIR,"scripts/output/thermometry/ca_opx_vs_ta98.pdf")
fig.savefig(outpath)

IPython.embed()
