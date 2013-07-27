from django.contrib.gis.db import models
from django.conf import settings
from picklefield.fields import PickledObjectField

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

	def assign_mineral(self):
		if self.Si/self.O > 1.75/6:
			if self.Ca/self.O > .5/6:
				self.mineral = "CPX"
			else:
				self.mineral = "OPX"
		if self.Si/self.O < 1./6:
			self.mineral = "SP"
			self.rebase(4)
		else:
			self.mineral = "OL"
			self.rebase(4)

	def rebase(self, formula_O=4):
		current = self.O
		ratio = formula_O/float(current)
		ls = settings.CATIONS + ["Total"] + [i+"_err" for i in settings.CATIONS]
		for i in ls:
			curr = getattr(self,i)
			setattr(self,i,curr*ratio)
		self.O = formula_O
		self.save()

