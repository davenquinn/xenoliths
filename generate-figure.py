#!/usr/bin/env python

from os import path
from subprocess import Popen, PIPE, STDOUT
from cairosvg import svg2pdf

from heatflow import results_dir

here = path.dirname(__file__)

data = results_dir("")

script = path.join(here,"scripts")

p = Popen(['coffee', script],stdin=PIPE)
p.communicate(input=data)
