from samples import models
from django.core.management.base import BaseCommand, CommandError
import IPython

class Command(BaseCommand):
	help = 'Calculates sample mineralogy.'
	#option_list = BaseCommand.option_list + (make_option("--output-format", dest="output_format", default=None),)
	def handle(self, *args, **options):
		for pt in models.Point.objects.all():
			for tag in pt.tags.names():
				if " " in [tag[0],tag[-1]]:
					pt.tags.remove(tag)
					pt.tags.add(tag.strip())
					pt.save()



