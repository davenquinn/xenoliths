from __future__ import division, print_function
import numpy as N
from ..application import app, db
from .models import ProbeMeasurement
from .group import get_cations
from .spinel import correct_spinel

mg_number = lambda c: c['Mg']/(c['Mg']+c['Fe'])
cr_number = lambda c: c['Cr']/(c['Cr']+c['Al'])

@app.with_context
def test_spinel_compositions():
    """
    See if we can recover compositions from spinel
    mineral equilibrium
    """
    q = (db.session.query(ProbeMeasurement)
            .filter_by(mineral='sp')
            .limit(100))
    for spinel in q.all():
        cat = get_cations(spinel, oxygen=4, uncertainties=True)
        cat_corr = correct_spinel(cat)
    assert N.allclose(cr_number(cat).n, cr_number(cat_corr).n)
    assert mg_number(cat).n <= mg_number(cat_corr).n
