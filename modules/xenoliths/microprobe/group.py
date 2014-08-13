
def get_oxides(queryset, oxygen=6, uncertainties=True):
	nobs = len(queryset)
	formula = {}
	for obj in queryset:
		oxs = obj.oxides
		for i,n in oxs.iteritems():
			formula[i] = formula.get(i,0)+n

	for key, item in formula.iteritems():
		formula[key] = item/nobs

	return formula

def get_cations(queryset, **kwargs):
	"""
	:param oxygen: oxygen basis for formula
	:param uncertainties: whether to use uncertainties in calculation
	"""
	try:
		nobs = len(queryset)
	except TypeError:
		return queryset.get_cations(**kwargs)
	formula = {}
	for obj in queryset:
		cats = obj.get_cations(**kwargs)
		for i,n in cats.iteritems():
			formula[i] = formula.get(i,0)+n

	for key, item in formula.iteritems():
		formula[key] = item/nobs

	return formula
