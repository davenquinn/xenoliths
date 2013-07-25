from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from samples.importer import import_all

class Command(BaseCommand):
	help = 'Imports measurement points to the project.'
	#option_list = BaseCommand.option_list + (make_option("--output-format", dest="output_format", default=None),)
	def handle(self, *args, **options):
		import_all()

		



