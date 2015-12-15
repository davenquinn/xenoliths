import operator
from flask import current_app
from ..converter import Converter

def oxygen_basis(mineral):
    if mineral in ["ol","sp"]:
        return 4
    else:
        return 6

def compute_molar(self):
    """ Computes the molar percentage of KNOWN products
        (i.e. unknown components not included).
    """
    def calculate(datum):
        molar_mass = datum.oxide.mass
        return datum.weight_percent/molar_mass

    values = [calculate(d) for d in self.data]
    total = sum(values)
    for d,v in zip(self.data,values):
        d.molar_percent = v/total*100

def compute_ratio(self, top, bottom):
    top = self.oxide(top).molar_percent
    bottom = self.oxide(bottom).molar_percent
    try:
        return 100*top/(top+bottom)
    except ZeroDivisionError:
        return float("NaN")

def compute_transform(self, system="pyroxene"):
    converter = Converter(system)
    molar = {i._oxide:i.molar_percent for i in self.data}
    return converter.transform(molar)

def compute_formula(meas, oxygen=6):
    formula = meas.__get_atomic__()
    scalar = oxygen/formula["O"]
    for key, value in formula.iteritems():
        formula[key] = value*scalar
    formula["Total"] = sum(formula.itervalues())
    return formula

def compute_mineral(point):
    """ Mineral totals from Taylor 1998
        We could multiply these ranges by two
        if it makes sense...
    """

    point.transforms = {k: compute_transform(point,k)
        for k in current_app.config["MINERAL_SYSTEMS"].keys()}

    t = point.transforms["minerals"]
    mineral = max(t.iteritems(), key=operator.itemgetter(1))[0]

    ## Recompute formula based on oxygen basis of minerals
    ofu = oxygen_basis(mineral)
    point.formula = compute_formula(point, ofu)

    cation_total = point.formula["Total"]-ofu
    if mineral == "ol":
        if not 2.99 < cation_total < 3.01:
            mineral = "na"
        if not 0.91 < point.formula["Si"] < 1.01:
            mineral = "na"

    if mineral in ["opx", "cpx"]:
        if not 3.975 < cation_total < 4.025:
            mineral = "na"

    point.mineral = mineral

def compute_derived(meas):
    compute_molar(meas)

    meas.mg_number = compute_ratio(meas,"MgO","FeO"),
    meas.cr_number = compute_ratio(meas,"Cr2O3","Al2O3")

    compute_mineral(meas)

    if meas.oxide_total < 90:
        meas.add_tag("bad")
    if meas.spot_size > 0:
        meas.add_tag("defocused")


