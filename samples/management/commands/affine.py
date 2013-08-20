import os
from optparse import make_option

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

from samples import data
from samples.models import Sample, Point
from samples.importer.array import Array
from samples.views import write_json


class Command(BaseCommand):
	help = 'Calculates sample mineralogy.'
	option_list = BaseCommand.option_list + (make_option("--sample", dest="sample", default=None),)

	def do_affine(self, sample):
		print sample.id
		arr = Array(sample.id+".dat")
		arr.transform_coordinates(sample.id+"_affine.txt")
		for rec in arr.each():
			try:
				point = Point.objects.get(sample=sample.id, n=int(rec.id))
			except ObjectDoesNotExist:
				print "Object {}_{} does not exist".format(sample, int(rec.id))
				continue

			point.geometry = rec.geometry()
			point.save()

	def handle(self, *args, **options):
		os.chdir(os.path.dirname(data.__file__))
		if options["sample"] is None:
			filter = Sample.objects.all()
		else:
			filter = Sample.objects.filter(id=options["sample"])
		for sample in filter:
			self.do_affine(sample)
		write_json()
		print "Done"




