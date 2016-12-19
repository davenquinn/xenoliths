from __future__ import print_function, division
import numpy as N
from xenoliths import app

from paper.text import tex_renderer, write_file
from paper.query import whole_rock_major_elements

def major_elements():
    oxides = app.config.get("OXIDES")
    oxides.remove("K2O")

    data = whole_rock_major_elements()

    template = tex_renderer.get_template("major-elements.tex")
    text = template.render(
        oxides=oxides,
        samples=data)
    write_file("build/major-elements.tex", text)

with app.app_context():
    major_elements()
