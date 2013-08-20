from models import Point

class Group(object):
	def __init__(self, *args, **kwargs):
		self.query = Point.objects.filter(**kwargs)

	def get_cations(self, oxygen=6, uncertainties=True):
		nobs = len(self.query)
		formula = {}
		for obj in self.query:
			cats = obj.get_cations(oxygen, uncertainties=uncertainties)
			for i,n in cats.iteritems():
				formula[i] = formula.get(i,0)+n

		for key, item in formula.iteritems():
			formula[key] = item/nobs

		return formula