from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from samples.models import Sample
from django.conf import settings
import numpy as N

def build_array(dataset):
	shape = (dataset['h'],dataset['w'])
	return N.array([d["v"] for d in dataset["values"]]).reshape(shape)

class Command(BaseCommand):
	help = 'Tests the calculation of oxide percents, with an option to fix if necessary.'
	option_list = BaseCommand.option_list + (make_option("-f", dest="fix", default=False),)
	def handle(self, *args, **options):
		query = Sample.objects.all()
		for sample in query:
			arr = build_array(sample.classification)

			
