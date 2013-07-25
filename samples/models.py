from django.contrib.gis.db import models
from django.conf import settings

# Create your models here.
class Sample(models.Model):
	id = models.CharField(max_length=4,primary_key=True)
	desc = models.TextField(blank=True)

class Point(models.Model):
	id = models.IntegerField(primary_key=True)
	geometry = models.PointField(blank=True, srid=900913)
	mineral = models.CharField(blank=True, max_length=20)
	mineral_edited = models.BooleanField(default=False)
	sample = models.ForeignKey(Sample)
	Si     = models.FloatField()
	Fe     = models.FloatField()
	Mg     = models.FloatField()
	Ti     = models.FloatField()
	Al     = models.FloatField()
	Na     = models.FloatField()
	Ca     = models.FloatField()
	Mn     = models.FloatField()
	Cr     = models.FloatField()
	Ni     = models.FloatField()
	Total  = models.FloatField()
	Si_err = models.FloatField()
	Fe_err = models.FloatField()
	Mg_err = models.FloatField()
	Ti_err = models.FloatField()
	Al_err = models.FloatField()
	Na_err = models.FloatField()
	Ca_err = models.FloatField()
	Mn_err = models.FloatField()
	Cr_err = models.FloatField()
	Ni_err = models.FloatField()
	O      = models.IntegerField()
	SiO2   = models.FloatField()
	FeO    = models.FloatField()
	MgO    = models.FloatField()
	TiO2   = models.FloatField()
	Al2O3  = models.FloatField()
	Na2O   = models.FloatField()
	CaO    = models.FloatField()
	MnO    = models.FloatField()
	Cr2O3  = models.FloatField()
	NiO    = models.FloatField()
	Ox_tot = models.FloatField()

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

