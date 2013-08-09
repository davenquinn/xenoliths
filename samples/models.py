from django.contrib.gis.db import models
from django.conf import settings
from picklefield.fields import PickledObjectField
import periodictable as pt
from django.conf import settings
from converter import Converter
import operator

# Create your models here.
class Sample(models.Model):
	id = models.CharField(max_length=4,primary_key=True)
	desc = models.TextField(blank=True)
	classification = PickledObjectField(blank=True, compress=True)

class Point(models.Model):
	uid = models.CharField(primary_key=True, max_length=10)
	id = models.IntegerField()
	geometry = models.PointField(blank=True, srid=900913)
	mineral = models.CharField(blank=True, max_length=4,choices=settings.MINERALS)
	sample = models.ForeignKey(Sample)
	oxides = PickledObjectField()
	errors = PickledObjectField()
	transforms = PickledObjectField()
	molar = PickledObjectField()
	formula = PickledObjectField()
	params = PickledObjectField()
	bad = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		compute_parameters = kwargs.pop("compute_parameters",False)
		if compute_parameters:
			self.molar = self.compute_molar()
			self.transforms = dict([(k,self.compute_transform(k)) for k in settings.MINERAL_SYSTEMS.keys()])
			self.compute_mineral()
			self.compute_params()
			self.formula = self.compute_formula(6)

		super(Point, self).save(*args, **kwargs)		

	def compute_molar(self):
		"""Computes the molar percentage of KNOWN products (i.e. unknown components not included)."""
		molar = {}
		for key, value in self.oxides.items():
			if key == 'Total': continue
			oxide = pt.formula(key)
			molar[key] = value/oxide.mass
		total = sum(molar.itervalues())
		for key, value in molar.iteritems():
			molar[key] = value/total*100
		molar["Total"] = 100
		return molar

	def compute_ratio(self, top, bottom):
		molar = self.molar
		if 0 in (molar[top],molar[bottom]):
			return None
		else:
			return 100*molar[top]/(molar[top]+molar[bottom])

	def compute_params(self):
		molar = self.molar
		params = {
			"Mg#": self.compute_ratio("MgO","FeO"),
			"Cr#": self.compute_ratio("Cr2O3","Al2O3")
		}
		self.params = params
		return params

	def compute_mineral(self):
		t = self.transforms["minerals"]
		mineral = max(t.iteritems(), key=operator.itemgetter(1))[0]
		self.mineral = mineral

	def compute_transform(self, system="pyroxene"):
		converter = Converter(system)
		return converter.transform(self.molar)

	def get_cations(self):
		formula = {}
		for key, molar_pct in self.molar.items():
			if key == "Total": continue
			oxide = pt.formula(key)
			for i,n in oxide.atoms.iteritems():
				if str(i) == "O": continue
				formula[str(i)] = formula.get(str(i),0)+n*molar_pct
		scalar = 100/sum(formula.itervalues())
		for key, value in formula.iteritems():
			formula[key] = value*scalar		
		formula["Total"] = sum(formula.itervalues())
		return formula	

	def compute_formula(self, oxygen=4):
		formula = {}
		for key, molar_pct in self.molar.items():
			if key == "Total": continue
			oxide = pt.formula(key)
			for i,n in oxide.atoms.iteritems():
				formula[str(i)] = formula.get(str(i),0)+n*molar_pct
		scalar = oxygen/formula["O"]
		for key, value in formula.iteritems():
			formula[key] = value*scalar
		formula["Total"] = sum(formula.itervalues())
		return formula
