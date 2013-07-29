from django.contrib.gis.db import models
from django.conf import settings
from picklefield.fields import PickledObjectField
import periodictable as pt
from django.conf import settings
from converter import Converter

# Create your models here.
class Sample(models.Model):
	id = models.CharField(max_length=4,primary_key=True)
	desc = models.TextField(blank=True)

class Point(models.Model):
	id = models.IntegerField(primary_key=True)
	geometry = models.PointField(blank=True, srid=900913)
	mineral = models.CharField(blank=True, max_length=20)
	sample = models.ForeignKey(Sample)
	oxides = PickledObjectField()
	errors = PickledObjectField()
	transforms = PickledObjectField()
	molar = PickledObjectField()

	def save(self, *args, **kwargs):
		compute_parameters = kwargs.pop("compute_parameters",False)
		if compute_parameters:
			self.molar = self.compute_molar()
			self.transforms = dict([(k,self.compute_transform(k)) for k in settings.MINERAL_SYSTEMS.keys()])
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

	def compute_transform(self, system="pyroxene"):
		converter = Converter.construct(system)
		return converter.transform(self.molar)

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
