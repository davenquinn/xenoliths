from django.shortcuts import render_to_response, RequestContext
from samples.models import Point
from django.conf import settings
import json
from interface import make_json

def filter_args(request):
	kwargs = dict()
	args = ["sample","mineral"]
	for a in args:
		s = request.GET.get(a,None)
		if s != None: kwargs[a] = s
	return kwargs

def table(request, type="oxide", sample=None, mineral=None):
	query = Point.objects.all()
	filterargs = dict()
	header_list = ["ID"]

	sample = request.GET.get("sample",None)
	mineral = request.GET.get("mineral", None)

	if sample != None: filterargs["sample"]=sample
	else: header_list.append("Sample")

	if mineral != None: filterargs["mineral"]=mineral
	else: header_list.append("Mineral") 

	query = Point.objects.filter(**filterargs)

	f = lambda x: "{0:.4f}".format(x)
	
	def shared_rows(obj):
		ls = [obj.id]
		if sample == None: ls.append(obj.sample.id)
		if mineral == None: ls.append(obj.mineral)
		return ls

	lines = []
	if type == "formula":
		headers = header_list+settings.CATIONS+["O","Total"]

		for obj in query:
			ls = shared_rows(obj)
			ls = ls+[f(getattr(obj,c)) for c in settings.CATIONS]+[obj.O,f(obj.Total)]

			line = "".join(["<td>{0}</td>".format(i) for i in ls])
			lines.append(line)

	if type == "oxides":
		headers = header_list+settings.OXIDES+["Total"]

		for obj in query:
			ls = shared_rows(obj)
			ls = ls+[f(getattr(obj,c)) for c in settings.OXIDES+["Ox_tot"]]

			line = "".join(["<td>{0}</td>".format(i) for i in ls])
			lines.append(line)

	if type == "errors":
		headers = header_list+settings.CATIONS
		for obj in query:
			ls = shared_rows(obj)
			ls = ls+[f(getattr(obj,c+"_err")) for c in settings.CATIONS]
			line = "".join(["<td>{0}</td>".format(i) for i in ls])
			lines.append(line)


	headline = "".join(["<th>{0}</th>".format(i) for i in headers])


	return render_to_response(
			'table.html',
			{"header": headline, "lines": lines},
			context_instance=RequestContext(request)
		)

def map(request, sample):

	mopts = settings.MAP_OPTIONS[sample]
	mopts["sample"] = sample

	context = {
		"sample": sample,
		"data": make_json(type="oxides",sample=sample,**filter_args(request)),
		"map_options": json.dumps(mopts)
	}

	return render_to_response(
			'map.html',
			context,
			context_instance=RequestContext(request)
		)		

def plot(request, type="oxides", axes="Ca-Mg"):
	elements = axes.split("-")
	if type == "oxides":
		oxides = [settings.OXIDES[settings.CATIONS.index(e)] for e in elements]

	types = {
		"oxides": {
			"title": "{0} vs. {1}".format(*tuple(oxides)),
			"script": "/static/js/plots/composition.js",
			"data":  make_json(type="oxides",**filter_args(request)),
			"config": json.dumps({"axes": {"x": oxides[1], "y": oxides[0]}})
		}
	}

	return render_to_response(
			'plot.html',
			types[type],
			context_instance=RequestContext(request)
		)	
