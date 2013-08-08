from jsonrpc import jsonrpc_method
from models import Sample, Point
import simplejson as json
import IPython
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

import simplejson

class PrettyFloat(float):
    def __repr__(self):
        return '%.8g' % self

def pretty_floats(obj):
    if isinstance(obj, float):
        return PrettyFloat(obj)
    elif isinstance(obj, dict):
        return dict((k, pretty_floats(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return map(pretty_floats, obj)             
    return obj

def make_json():
	"""Makes geojson for the measurements"""
	samples = Sample.objects.all()
	query = Point.objects.all()
	output = []
	for obj in query:
		i = {
			"type": "Feature",
			"properties": {
				"mineral": obj.mineral,
				"sample": obj.sample.id,
				"systems": obj.transforms,
				"oxides": obj.oxides,
				"formula": obj.formula,
				"molar": obj.molar,
				"id": obj.id,
				"params": obj.params,
				"flags": {
					"bad": obj.bad,
					"review": False
				}
			},
			"geometry": json.loads(obj.geometry.json)
		}
		output.append(i)
	output = {
		"type": "FeatureCollection",
		"features": output,
		"properties": {
			"samples": [obj.id for obj in samples]
		}
	}
	return output

@jsonrpc_method('get_classification')
def get_classification(request, sample):
	sample = Sample.objects.get(id=sample)
	s = sample.classification
	if s == "": s = False
	return s

@jsonrpc_method('save_classification')
def save_classification(request, sample, classification):
	try:
		sample = Sample.objects.get(id=sample)
		sample.classification = classification
		sample.save()
		return True
	except:
		return False

@jsonrpc_method('get_data')
def get_data(request):
	return make_json()
	
@cache_page(60*60)
def data(request):
	return HttpResponse(json.dumps(pretty_floats(make_json())), mimetype="application/json")