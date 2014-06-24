import os
from jsonrpc import jsonrpc_method
from models import Sample, Point
import simplejson as json
import IPython
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.http import HttpRequest
from django.utils.cache import get_cache_key

def expire_cache():
    """
    This function allows you to invalidate any view-level cache.
        view_name: view function you wish to invalidate or it's named url pattern
        args: any arguments passed to the view function
        namepace: optioal, if an application namespace is needed
        key prefix: for the @cache_page decorator for the function (if any)
    """
    request = HttpRequest()

    request.path = reverse(data)
    key = get_cache_key(request)
    if key:
        if cache.get(key):
            cache.set(key, None, 0)
        return True
    return False

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
				"id": obj.n,
				"params": obj.params,
				"tags": [str(tag) for tag in obj.tags.all()]
			},
			"geometry": json.loads(obj.geometry.json)
		}
		output.append(i)
	output = {
		"type": "FeatureCollection",
		"features": output,
	}
	return output

def write_json(path=None):
	if path is None:
		path = os.path.join(settings.SITE_DIR,"frontend","data.json")
	with open(path, "w") as f:
		json.dump(pretty_floats(make_json()), f)

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

@jsonrpc_method('add_tag')
def add_tag(request, tag, points):
	for point in points:
		pt = Point.objects.get(sample=point[0], n=point[1])
		pt.tags.add(tag)

@jsonrpc_method('remove_tag')
def remove_tag(request, tag, points):
	for point in points:
		pt = Point.objects.get(sample=point[0], n=point[1])
		pt.tags.remove(tag)

@jsonrpc_method('get_data')
def get_data(request):
	return make_json()

@cache_page(10)
def data(request):
	return HttpResponse(json.dumps(pretty_floats(make_json())), mimetype="application/json")
