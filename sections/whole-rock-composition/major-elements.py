from __future__ import print_function, division
import numpy as N
from xenoliths import app
from sys import argv

from figurator import tex_renderer, write_file
from paper.query import whole_rock_major_elements

def major_elements():
    oxides = app.config.get("OXIDES")

    data = whole_rock_major_elements()

    template = tex_renderer.get_template(argv[1])
    text = template.render(
        oxides=oxides,
        samples=data)
    write_file(argv[2], text)

with app.app_context():
    major_elements()
