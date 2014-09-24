from collections import defaultdict

def get_oxides(queryset, oxygen=6, uncertainties=True):
	nobs = len(queryset)
	formula = defaultdict(int)
	for obj in queryset:
		for i,n in obj.oxides.iteritems():
			formula[i] += n/nobs
	return defaultdict(lambda: float("NaN"),formula)

def get_cations(queryset, **kwargs):
	"""
	:param oxygen: oxygen basis for formula
	:param uncertainties: whether to use uncertainties in calculation
	"""
	try:
		nobs = len(queryset)
	except TypeError:
		return queryset.get_cations(**kwargs)
	formula = defaultdict(int)
	for obj in queryset:
		cats = obj.get_cations(**kwargs)
		for i,n in cats.iteritems():
			formula[i] += n/nobs
	return defaultdict(lambda: float("NaN"),formula)
