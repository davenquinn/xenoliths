from __future__ import division, print_function

from sys import argv
from depletion_model import depletion_degrees
from figurator import tex_renderer, write_file

sample_data = depletion_degrees()

text = (tex_renderer
    .get_template("depletion_degrees.tex")
    .render(samples=sample_data))

write_file(argv[2], text)

