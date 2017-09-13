#!/usr/bin/env python

from xenoliths import app
from paper.query import xenolith_minerals
from figurator import tex_renderer, write_file

def mineral_compositions():
    """
    Creates a table of the average composition of
    each of the mineral components in each Xenolith sample.
    Could potentially be combined with modal abundance
    data, but might not be best.
    """
    oxides = [ox
        for ox in app.config.get("OXIDES")
        if ox != "K2O"]

    text = (tex_renderer
        .get_template("minerals.tex")
        .render(
            ncols=len(oxides)+5,
            oxides=oxides,
            samples=xenolith_minerals("weight")))
    write_file("build/minerals.tex", text)

with app.app_context():
    mineral_compositions()

