#!/usr/bin/env python
"""
Runs a coffeescript figure-generation
routine with the name of the heatflow
results path
"""
from sys import argv
from os import path
from subprocess import Popen, PIPE, STDOUT
from cairosvg import svg2pdf

from heatflow import results_dir

here = path.dirname(__file__)

data = results_dir("")

p = Popen(['coffee', argv[1]],stdin=PIPE)
p.communicate(input=data)
