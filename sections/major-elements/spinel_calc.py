from __future__ import division, print_function

from xenoliths.microprobe.group import get_cations

_tetrahedral = ('Cr','Al','Si', 'Ti','Fe(III)')

tetrahedral = lambda c: sum(
    i for k,i in c.items()
    if k in _tetrahedral)
octahedral = lambda c: sum(
    i for k,i in c.items()
    if k not in _tetrahedral)

def oxygens(cation):
    # Ignore silicon for oxygen calculation
    if cation in ['Si','Ti']:
        return 2
    elif cation in _tetrahedral:
        return 1.5
    else:
        return 1

def align_oxygen(cat, silent=False):
    # Tamp down excess oxygen
    n_ox = sum(oxygens(k)*v for k,v in cat.items())
    cat = {k:v*4/n_ox for k,v in cat.items()}

    cation_total = sum(cat.values())
    if not silent:
        print(cation_total,n_ox)
    return cat


def correct_spinel(obj, **kwargs):
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
        cat = get_cations(obj, oxygen=4, **kwargs)

    cat['Fe(III)'] = 0

    for i in range(500):
        oct = octahedral(cat)
        # There should only be one octahedral cation
        excess_oct = oct-1
        if excess_oct < 0:
            # We can't do any more without cannibalizing
            # the octahedral site.
            break

        Fe = cat['Fe']
        if excess_oct > Fe:
            # We only consider iron as excess, as it can
            # be 
            excess_oct = Fe
        removable_iron = excess_oct
        factor = 0.885 # not sure where this factor comes from
        # but I've seen it before
        cat['Fe(III)'] += removable_iron*factor
        cat['Fe'] -= excess_oct*factor

        cat = align_oxygen(cat, silent=True)

        cation_total = sum(cat.values())
        if abs(cation_total - 3) < 0.00001:
            break

    cat = align_oxygen(cat, silent=True)
    return cat

