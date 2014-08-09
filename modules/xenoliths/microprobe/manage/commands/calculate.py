from samples import models
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	help = 'Calculates sample mineralogy.'
	#option_list = BaseCommand.option_list + (make_option("--output-format", dest="output_format", default=None),)
	def handle(self, *args, **options):
		for m in models.Point.objects.all():
			m.assign_mineral()
			m.save()



