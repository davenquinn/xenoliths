from ..application import app, db
from .models import ProbeDatum, ProbeMeasurement
from .group import get_cations, get_molar

def compute_spinel_cations(spinel):
    """
    We compute the ideal cation composition of a spinel
    to derive Fe(II)/Fe(III) ratio, for the eventual
    calculation of a meaningful Mg#.

    Al,Fe(III),Cr, Ti, Si* are included in the tetrahedral site

    Mg, Fe(II), Mn, Ni, Ca* are included in the octahedral site

    *trace/contaminant
    """

    cat = get_cations(spinel, oxygen=4, uncertainties=True)

    tetrahedral = ('Cr','Al','Si', 'Ti')

    total_iron = cat.pop('Fe')
    total_tetrahedral = sum(
        i for k,i in cat.items()
        if k in tetrahedral)
    total_octahedral = sum(
        i for k,i in cat.items()
        if k not in tetrahedral)

    # Iron that can't fit into octahedral site
    tetrahedral_iron = 2 - total_tetrahedral
    octahedral_iron = total_iron - tetrahedral_iron

    assert octahedral_iron >= 0
    assert tetrahedral_iron >= 0

    cat['Fe2'] = octahedral_iron
    cat['Fe3'] = tetrahedral_iron

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
        cations = compute_spinel_cations(spinel)
        print(cations)
    assert False
