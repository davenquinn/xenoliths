import operator
from ...application import app
from ..converter import Converter

def oxygen_basis(mineral):
    if mineral in ["ol","sp"]:
        return 4
    else:
        return 6

def compute_molar(self, session):
    """Computes the molar percentage of KNOWN products
    (i.e. unknown components not included)."""
    def calculate(datum):
        molar_mass = datum.oxide.mass
        return datum.weight_percent/molar_mass

    values = [calculate(d) for d in self.data]
    total = sum(values)
    for d,v in zip(self.data,values):
        d.molar_percent = v/total*100
        session.add(d)

def compute_ratio(self, top, bottom):
    datum = lambda n: self.data.filter_by(_oxide=n).first()
    top = datum(top).molar_percent
    bottom = datum(bottom).molar_percent
    try:
        return 100*top/(top+bottom)
    except ZeroDivisionError:
        return float("NaN")

def compute_transform(self, system="pyroxene"):
    converter = Converter(system)
    return converter.transform(self.molar)

def compute_formula(meas, oxygen=6):
    formula = meas.__get_atomic__()
    scalar = oxygen/formula["O"]
    for key, value in formula.iteritems():
        formula[key] = value*scalar
    formula["Total"] = sum(formula.itervalues())
    return formula

def compute_mineral(point):
    """Mineral totals from Taylor 1998, adjusted to be slightly more forgiving"""

    point.transforms = {k: compute_transform(point,k)
        for k in app.config["MINERAL_SYSTEMS"].keys()}

    t = point.transforms["minerals"]
    mineral = max(t.iteritems(), key=operator.itemgetter(1))[0]

    ## Recompute formula based on oxygen basis of minerals
    ofu = oxygen_basis(mineral)
    point.formula = compute_formula(point, ofu)

    cation_total = point.formula["Total"]-ofu
    if mineral == "ol":
        if not 2.98 < cation_total < 3.02:
            mineral = "na"
        if not 0.98 < point.formula["Si"] < 1.02:
            mineral = "na"

    if mineral in ["opx", "cpx"]:
        if not 3.97 < cation_total < 4.03:
            mineral = "na"

    point.mineral = mineral

def compute_derived(meas, session):
    compute_molar(meas, session)

    meas.mg_number = compute_ratio(meas,"MgO","FeO"),
    meas.cr_number = compute_ratio(meas,"Cr2O3","Al2O3")

    compute_mineral(meas)

    if meas.oxide_total < 90:
        meas.add_tag("bad")

    session.add(meas)

