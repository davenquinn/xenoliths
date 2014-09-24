#!/usr/bin/env python
from __future__ import division

from flask import Blueprint, Response, render_template
from cStringIO import StringIO
from .rare_earth.plot import plot_DREE
from .rare_earth.calc import prepare_data, big10, rare_earths
from ..core.models import Sample

thermometry = Blueprint(
	'Thermometry',
	__name__,
	static_folder="static",
	template_folder="templates")

@thermometry.route("/ree/")
def ree():
	return "Hello, world."

@thermometry.route("/ree_<sample>.svg")
def ree_opx(sample):
	sample = Sample.query.get(sample)
	fig = plot_DREE(sample)
	imgdata = StringIO()
	fig.savefig(imgdata, format="svg")
	imgdata.seek(0)
	return Response(imgdata.read(), mimetype="image/svg+xml")

@thermometry.route("/ree/input")
def table():
	def inner():
		first = ["ID"]+big10+rare_earths+[" "]+big10+rare_earths
		yield ", ".join(first)
		for sample in Sample.query.all():
			d = prepare_data(sample)
			a = [sample.id]+d["major"]["cpx"]+d["trace"]["cpx"]+[""]+d["major"]["opx"]+d["trace"]["opx"]
			yield ", ".join([str(i) for i in a])
	a = "\n".join(list(inner()))
	return Response(a, mimetype='text')
