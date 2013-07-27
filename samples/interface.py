from models import Point
from django.conf import settings
import json
import numpy as N

def get_json(request, type="formula"):
	pass

def make_json(*args, **kwargs):
	"""Makes geojson for the measurements"""
	type = kwargs.pop("type", "oxides")
	query = Point.objects.all().filter(**kwargs)

	output = []
	for obj in query:
		a = {
			"mineral": obj.mineral,
			"sample": obj.sample.id
		}
		if type in ["oxides","both"]:
			a["oxides"] = obj.oxides

		i  = {
			"id": obj.id,
			"type": "Feature",
			"properties": a,
			"geometry": json.loads(obj.geometry.json)
		}
		output.append(i)
	output = {
		"type": "FeatureCollection",
		"features": output
	}
	return json.dumps(output)

def make_array(*args, **kwargs):
	"""Makes a numpy record-array of the returned queryset."""
	type = kwargs.pop("type", "oxides")
	query = Point.objects.all().filter(**kwargs)
	objects = list(query)
	return N.core.records.array(objects, names=settings.OXIDES)

