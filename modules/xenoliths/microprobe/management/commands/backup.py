from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from samples.views import write_json
from datetime import datetime
import os
from django.conf import settings

class Command(BaseCommand):
	help = 'Imports measurement points to the project.'
	#option_list = BaseCommand.option_list + (make_option("--output-format", dest="output_format", default=None),)
	def handle(self, *args, **options):
		"""Backs up data for all the measurements"""
		now = datetime.now().strftime("%Y-%m-%d_%H:%M")
		path = os.path.join(settings.SITE_DIR,"samples","data","backup","{}.json".format(now))
		write_json(path)