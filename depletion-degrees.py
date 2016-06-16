from __future__ import division, print_function

from sys import argv
import numpy as N
from xenoliths import app
from depletion_model import sample_ree
from depletion_model.util import element, ree_only
from depletion_model import DepletionModel
from paper.query import whole_rock_major_elements
from pandas import concat
from paper.text import tex_renderer, write_file

with app.app_context():
    ree_data = sample_ree(normalized=True)
    major_element_data = whole_rock_major_elements(dataframe=True)
model = DepletionModel(argv[1])

ree_fit = model.fit_HREE(ree_data)

# Solid composition data is in %wt of solid component
Mg_fit = model.fit('Solid Composition',major_element_data,'MgO')
Al_fit = model.fit('Solid Composition',major_element_data,'Al2O3')

def series():
    """
    Rename series for consistency
    """
    fits = (ree_fit,Mg_fit,Al_fit)
    names = ('ree','MgO','Al2O3')

    for fit, name in zip(fits,names):
        s = fit['mass']
        s.name = name
        yield s

masses = concat(list(series()),axis=1)
depletion = (100-masses).reset_index()

text = (tex_renderer
    .get_template("depletion_degrees.tex")
    .render(samples=[r.to_dict()
        for i,r in depletion.iterrows()]))

write_file(argv[2], text)

