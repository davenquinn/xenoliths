import numpy as N
from xenoliths.application import app, db
from xenoliths.core.models import Sample
from xenoliths.SIMS.query import sims_data, element_data
from paper.text import tex_renderer, write_file
import periodictable as pt

def create_table():
    data = sims_data(whole_rock=True)
    elements = data.index.get_level_values('symbol').unique()

    data = element_data(data, columns='symbol')

    d = data.reset_index()
    min_data = {k: d[d['mineral'] == k].iterrows()
            for k in ('opx','cpx','whole_rock')}

    text = (tex_renderer
        .get_template("trace-elements.tex")
        .render(
            ncols=len(elements)+2,
            elements=elements,
            **min_data))
    write_file("build/trace-elements.tex",text)

with app.app_context():
    create_table()
