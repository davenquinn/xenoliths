from __future__ import division, print_function

import numpy as N
from ..application import app, db
from .models import ProbeDatum, ProbeMeasurement
from .group import get_cations, get_molar

_tetrahedral = ('Cr','Al','Si', 'Ti','Fe(III)')

tetrahedral = lambda c: sum(
    i for k,i in c.items()
    if k in _tetrahedral)
octahedral = lambda c: sum(
    i for k,i in c.items()
    if k not in _tetrahedral)

mg_number = lambda c: c['Mg']/(c['Mg']+c['Fe'])
cr_number = lambda c: c['Cr']/(c['Cr']+c['Al'])

def oxygens(cation):
    # Ignore silicon for oxygen calculation
    if cation == 'Si':
        return 2
    elif cation in _tetrahedral:
        return 1.5
    else:
        return 1

def correct_spinel(obj):
    """
    We compute the ideal cation composition of a spinel
    to derive Fe(II)/Fe(III) ratio, for the eventual
    calculation of a meaningful Mg#.

    Al,Fe(III),Cr, Ti, Si* are included in the tetrahedral site

    Mg, Fe(II), Mn, Ni, Ca* are included in the octahedral site

    *trace/contaminant
    """
    try:
        obj['Fe']
        cat = obj
    except TypeError:
        cat = get_cat(obj, oxygen=4, uncertainties=True)

    cat['Fe(III)'] = 0

    for i in range(500):
        oct = octahedral(cat)
        excess_oct = oct-1
        if excess_oct > 0:
            Fe = cat['Fe']
            if excess_oct > Fe: excess_oct = Fe
            removable_iron = excess_oct*2/3
            cat['Fe(III)'] += removable_iron
            cat['Fe'] -= removable_iron
        else:
            # We can't do any more without cannibalizing
            # the octahedral site.
            break

        n_ox = sum(oxygens(k)*v for k,v in cat.items())
        cat = {k:v*4/n_ox for k,v in cat.items()}
        total = sum(cat.values())
        if abs(total - 3) < 0.00001:
            break
    return cat

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
