#!/usr/bin/env python
from __future__ import division

from flask import Blueprint, Response, render_template
from cStringIO import StringIO
from .results import sample_temperatures
from .rare_earth.plot import plot_DREE, ree_temperature
from .rare_earth.calc import prepare_data, big10, rare_earths
from ..core.models import Sample

thermometry = Blueprint(
	'Thermometry',
	__name__,
	static_folder="static",
	template_folder="templates")

filter_samples = lambda x: len(x.sims_measurements) > 0

def prepare_data(sample):
	t = sample_temperatures(sample)
	return dict(
		sample=sample,
		ree= ree_temperature(sample,
			pressure=1.5,
			uncertainties=True),
		bkn=t["core"]["bkn"]["single"]["val"],
		ta98=t["core"]["ta98"]["single"]["val"])

@thermometry.route("/")
def index():
	samples = filter(filter_samples, Sample.query.all())
	data = map(prepare_data, samples)

	return render_template("thermometry/list.html",
		title="Thermometry results (core grains)",
		data=data)

@thermometry.route("/ree/<sample>.svg")
def ree_opx(sample):
	sample = Sample.query.get(sample)
	fig = plot_DREE(sample)
	imgdata = StringIO()
	fig.savefig(imgdata, format="svg")
	imgdata.seek(0)
	return Response(imgdata.read(), mimetype="image/svg+xml")

@thermometry.route("/ree/excel-input")
def table():
	def inner():
		first = ["ID"]+big10+rare_earths+[" "]+big10+rare_earths
		yield ", ".join(first)
		samples = filter(filter_samples, Sample.query.all())
		for sample in samples:
			d = prepare_data(sample)
			a = [sample.id]+d["major"]["cpx"]+d["trace"]["cpx"]+[""]+d["major"]["opx"]+d["trace"]["opx"]
			yield ", ".join([str(i) for i in a])
	a = "\n".join(list(inner()))
	return Response(a, mimetype='text')

@thermometry.route("/ree-ta98.svg")
def comparison():
	return "Hello"
