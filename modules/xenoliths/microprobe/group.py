from __future__ import print_function, division
from collections import defaultdict
from sqlalchemy.sql import func
from .models import ProbeDatum, ProbeMeasurement, db, FORMULAE
from uncertainties import ufloat
import periodictable as pt
from functools import partial

def get_quantity(quantity, queryset, **kwargs):
    try:
        q = queryset.with_entities(ProbeMeasurement.id)
        filt = ProbeDatum.measurement_id.in_(q)
    except AttributeError:
        filt = ProbeDatum.measurement_id == queryset.id

    mol = ProbeDatum.molar_percent
    average = func.avg(quantity)
    qvars = [ProbeDatum._oxide,
            average.label('avg')]

    uncertainties = kwargs.pop("uncertainties",False)
    if uncertainties:
        e = ProbeDatum.error
        sum_ = func.sum(func.pow(e*quantity/100,2))
        std = func.sqrt(sum_)/func.count("*")
        qvars.append(std.label("analytic_std"))

        std2 = func.stddev(quantity)
        qvars.append(std2.label("sample_std"))

    data = db.session.query(*tuple(qvars))\
                .filter(filt)\
                .group_by(ProbeDatum._oxide)\
                .all()

    if uncertainties:
        try:
            return {o:ufloat(n,a+s) for o,n,a,s in data}
        except TypeError:
            return {o:ufloat(n,a) for o,n,a,s in data}
    else:
        return {o:n for o,n in data}

def get_number(property, queryset):
    """
    Gets a calculated parameter (e.g. oxide total, mg_number, cr_number)
    from the queryset. The parameter will not take into account errors
    from uncertainties on individual measurements.
    """
    values = queryset.with_entities(
        func.avg(property),func.stddev(property))
    n,s = values.all()[0]
    if s == None: s = 0
    return ufloat(n,s)

get_oxides = partial(get_quantity, ProbeDatum.weight_percent)
get_normalized_oxides = partial(get_quantity, ProbeDatum.weight_percent*100/ProbeMeasurement.oxide_total)
get_molar = partial(get_quantity, ProbeDatum.molar_percent)

def average_composition(queryset, **kwargs):
    """
    The average oxide composition of a queryset, calculated in
    one of several ways (either wt%, molar%, or normalized wt% abundances).
    Returns the same result as the partial functions above, but is a bit
    more descriptive.

    :param type: Options
        - weight              Oxide weight % (default)
        - normalized_weight   Oxide weight % (normalized to 100% abundances)
        - molar               Oxide molar %
    :param uncertainties:     Whether to include uncertainties (default FALSE)
    """
    mapping = dict(
        weight=ProbeDatum.weight_percent,
        normalized_weight=ProbeDatum.weight_percent*100/ProbeMeasurement.oxide_total,
        molar=ProbeDatum.molar_percent)
    try:
        q = mapping[kwargs.pop("type","weight")]
    except KeyError:
        raise ArgumentError("Parameter `type` must be either"
                "`weight`,`molar`, or `normalized_weight`")

    return get_quantity(q,queryset, **kwargs)


get_mg_number = partial(get_number, ProbeMeasurement.mg_number)
get_cr_number = partial(get_number, ProbeMeasurement.cr_number)
get_oxide_total = partial(get_number, ProbeMeasurement.oxide_total)

def get_cations(queryset, **kwargs):
    """
    Get cations using SQL query magic
    :param oxygen: oxygen basis for formula
    :param uncertainties: whether to use uncertainties in calculation
    """
    oxygen_basis = kwargs.pop("oxygen",6)

    molar = {FORMULAE[ox]: v\
            for ox,v in get_molar(queryset, **kwargs).items()}
    f_oxygen = sum([ox.atoms[pt.O]*v for ox,v in molar.items()])
    scalar = oxygen_basis/f_oxygen

    formula = defaultdict(int)
    for ox,v in molar.items():
        for i, n in ox.atoms.items():
            if i == pt.O: continue
            formula[str(i)] += n*v*scalar
    return defaultdict(lambda: float("NaN"),formula)

def iterate_cations(queryset, **kwargs):
    """
    Get cations iteratively. This is slow but known to work
    :param oxygen: oxygen basis for formula
    :param uncertainties: whether to use uncertainties in calculation
    """
    nobs = queryset.count()
    formula = defaultdict(int)
    for obj in queryset.all():
        cats = obj.get_cations(**kwargs)
        for i,n in cats.iteritems():
            formula[i] += n/nobs
    return defaultdict(lambda: float("NaN"),formula)

