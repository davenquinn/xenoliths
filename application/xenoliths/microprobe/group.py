
from collections import defaultdict
from sqlalchemy.sql import func
from .models import ProbeDatum, ProbeMeasurement, db, FORMULAE
from uncertainties import ufloat
import numpy as N
import periodictable as pt
from functools import partial

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

    type = kwargs.pop("type","weight")

    try:
        quantity = mapping[type]
    except KeyError:
        raise ArgumentError("Parameter `type` must be either"
                "`weight`,`molar`, or `normalized_weight`")

    try:
        q = queryset.with_entities(ProbeMeasurement.id)
        filt = ProbeDatum.measurement_id.in_(q)
    except AttributeError:
        filt = ProbeDatum.measurement_id == queryset.id

    average = func.avg(quantity)
    qvars = [ProbeDatum._oxide,
            average.label('avg')]

    uncertainties = kwargs.pop("uncertainties",False)
    if uncertainties:
        e = ProbeDatum.error
        sum_ = func.sum(func.pow(e/100*quantity,2))
        std = func.sqrt(sum_)/func.count("*")
        qvars.append(std.label("analytic_std"))

        std2 = func.stddev(quantity)

        qvars.append(std2.label("sample_std"))

    data = db.session.query(ProbeDatum)\
        .join(ProbeMeasurement)\
        .filter(filt)\
        .with_entities(*tuple(qvars))\
        .group_by(ProbeDatum._oxide)\
        .all()

    if uncertainties:
        try:
            return {o:ufloat(n,a+s) for o,n,a,s in data}
        except TypeError:
            return {o:ufloat(n,a) for o,n,a,s in data}
    else:
        return {o:n for o,n in data}

get_oxides = partial(average_composition, type="weight")
get_normalized_oxides = partial(average_composition, type="normalized_weight")
get_molar = partial(average_composition, type="molar")

get_mg_number = partial(get_number, ProbeMeasurement.mg_number)
get_cr_number = partial(get_number, ProbeMeasurement.cr_number)
get_oxide_total = partial(get_number, ProbeMeasurement.oxide_total)

mg_number = get_mg_number
cr_number = get_cr_number
oxides = get_oxides
oxide_total = get_oxide_total

def get_cations(queryset, **kwargs):
    """
    Get cations using SQL query magic
    :param oxygen: oxygen basis for formula
    :param uncertainties: whether to use uncertainties in calculation
    """
    oxygen_basis = kwargs.pop("oxygen",6)

    molar = get_molar(queryset, **kwargs)

    formula = defaultdict(int)
    for oxide,v in molar.items():
        # We eliminated a complex unhashably-keyed dict here.
        # This may become the focus of new errors but we will have to see
        ox = FORMULAE[oxide]
        for i, n in ox.atoms.items():
            formula[str(i)] += n*v

    # Rescale cation abundances to the oxygen basis
    ox = formula.pop("O")
    scalar = oxygen_basis/ox

    return {k:v*scalar for k,v in formula.items()}

def iterate_cations(queryset, **kwargs):
    """
    Get cations iteratively. This is slow but known to work
    :param oxygen: oxygen basis for formula
    :param uncertainties: whether to use uncertainties in calculation
    """
    oxygen = kwargs.pop("oxygen",6)

    nobs = queryset.count()
    formula = defaultdict(list)
    for obj in queryset.all():
        cats = obj.get_cations(oxygen=oxygen, **kwargs)
        for k,n in cats.items():
            formula[k].append(n)
    del formula["Total"]

    output = dict()
    for ox,ls in list(formula.items()):
        u = N.mean(ls)
        if hasattr(u, "nominal_value"):
            s_sample = N.std([l.n for l in ls])
            u = ufloat(u.n,u.s+s_sample)
        output[ox] = u
    return output
