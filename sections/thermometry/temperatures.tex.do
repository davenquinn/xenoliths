#!/usr/bin/env python

import numpy as N
from uncertainties import ufloat
from figurator import tex_renderer, write_file
from xenoliths import app
from data import ree_data, summary_data
from dofile import redo_ifchange
from sys import argv

# This could be more concise, maybe
redo_ifchange('templates/temperature.tex')
template = tex_renderer.get_template("temperature.tex")

with app.app_context():
    text = template.render(samples=summary_data())
    write_file(argv[3], text)

