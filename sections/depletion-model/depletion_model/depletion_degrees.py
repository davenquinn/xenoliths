from __future__ import division, print_function

from sys import argv
import numpy as N
from xenoliths import app
from . import sample_ree, DepletionModel
from .util import element, ree_only
from paper.query import whole_rock_major_elements, xenolith_minerals
from pandas import concat, DataFrame
from figurator import tex_renderer, write_file

def get_spinel_data(sample):
    data = sample['sp']
    return dict(
        id = sample['id'],
        **data['normalized_weight'])

def depletion_degrees():
    with app.app_context():
        ree_data = sample_ree(normalized=True)
        major_element_data = whole_rock_major_elements(dataframe=True)
        mineral_data = xenolith_minerals("normalized_weight")
    model = DepletionModel(argv[1])

    _ = [get_spinel_data(s) for s in mineral_data]
    spinel_data = DataFrame.from_dict(_).set_index('id')

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

    return [r.to_dict() for i,r in depletion.iterrows()]

