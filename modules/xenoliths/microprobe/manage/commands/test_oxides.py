from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from samples.models import Point
from django.conf import settings
from math import fabs

class Command(BaseCommand):
	help = 'Tests the calculation of oxide percents, with an option to fix if necessary.'
	option_list = BaseCommand.option_list + (make_option("-f", dest="fix", default=False),)
	def handle(self, *args, **options):
		query = Point.objects.all()
		for obj in query:
			a = 0
			for cat in settings.CATIONS:
				a += getattr(obj,cat)
			a += obj.O
			dif = a-obj.Total
			if fabs(dif) > .0001:
				print obj.id, dif
				if options["fix"]:
					obj.O = 4
					obj.save()		



