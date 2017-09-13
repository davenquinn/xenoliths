#!/usr/bin/env python

from xenoliths import app
from paper.query import xenolith_minerals
from figurator import tex_renderer, write_file
from sys import argv

def mineral_compositions():
    """
    Creates a table of the average composition of
    each of the mineral components in each Xenolith sample.
    Could potentially be combined with modal abundance
    data, but might not be best.
    """
    oxides = app.config.get("OXIDES")

    text = (tex_renderer
        .get_template(argv[1])
        .render(
            ncols=len(oxides)+5,
            oxides=oxides,
            samples=xenolith_minerals("weight")))
    write_file(argv[2], text)

with app.app_context():
    mineral_compositions()

