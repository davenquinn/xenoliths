from __future__ import print_function, division

from sqlalchemy.sql import func
from uncertainties import ufloat, umath
from uncertainties import unumpy
from uncertainties.unumpy import uarray
import numpy as N
from collections import defaultdict

from ..application import app, db
from .models import ProbeDatum, ProbeMeasurement
from .group import get_oxides, get_molar, get_cations, iterate_cations, average_composition

def allclose_uncertain(a,b, **kwargs):
    a = (N.allclose(a.n, b.n, **kwargs),N.allclose(a.s, b.s, **kwargs))
    return all(a)

@app.with_context
def test_oxides():
    # Filter a single xenolith because some samples have
    # different oxides measured
    filter = ProbeMeasurement.sample_id == "CK-4"

    q = db.session.query(ProbeMeasurement).filter(filter)
    data = get_oxides(q, uncertainties=False)
    s = sum(data.values())
    _ = func.sum(ProbeMeasurement.oxide_total)/func.count("*")
    d = (q.with_entities(_)).scalar()
    print(s,d)
    assert N.allclose(s, d)

@app.with_context
def test_molar():
    """
    Tests that molar percentages always sum to 100
    """
    queryset = ProbeMeasurement.query\
        .filter(ProbeMeasurement.sample_id == "CK-4")\
        .filter(ProbeMeasurement.mineral == "opx")
    data = get_molar(queryset, uncertainties=False)
    s = sum(data.values())
    print(s)
    assert N.allclose(s, 100)

@app.with_context
def test_cations():
    """ Tests that cation proportions computed using SQL
        are functionally the same as iteratively computed
        values.
    """
    queryset = ProbeMeasurement.query\
        .filter(ProbeMeasurement.id < 100)
    g = get_cations(queryset, uncertainties=True)
    d = iterate_cations(queryset, uncertainties=True)

    sums = tuple(sum(i.values()).n for i in (g,d))
    print(*sums)
    assert N.allclose(*sums, rtol=0.1)

    for k in g.keys():

        print(k, g[k], d[k])
        assert N.allclose(g[k].n, d[k].n, atol=0.1)
        assert N.allclose(g[k].s, d[k].s, rtol=2)

def test_uncertainties():
    """ Tests the method used to calculate uncertainties in
        SQL
        Note: this tests uncertainties on the calculation of
        the mean itself!
    """
    # Build array of 100 values
    n = 100
    arr = N.random.randn(2,n)
    arr[1] = 0.1*N.abs(arr[1])
    unc = uarray(arr[0],arr[1])
    avg = N.mean(unc)

    # Test uncertainties in the calculation of the mean of
    # the distribution
    k = arr[0].mean()
    s = N.sqrt(N.sum(arr[1]**2))/n
    avg2 = ufloat(k,s)
    print(avg,avg2)
    assert N.allclose(avg.n,avg2.n)
    assert N.allclose(avg.s, avg2.s)

    # Test uncertainties in the calculation of a single
    # measured value fo the distribution
    mu = unc.mean()
    # Shim for standard deviation
    variance = N.mean((unc-avg)**2)+mu.s**2
    avg = ufloat(mu.n, umath.sqrt(variance).n)

    k = arr[0].mean()
    s = N.sqrt(N.sum(arr[1]**2))/n
    s = arr[0].std()+s
    avg2 = ufloat(k,s)

    print(avg,avg2)
    assert N.allclose(avg.n,avg2.n, rtol=0.5)
    assert N.allclose(avg.s, avg2.s, rtol=0.5)

def naive_composition(queryset, **kwargs):
    """
    Provides a naive but slow alternative to
    computation of grouped measurements using
    the `average_composition` method. Same interfacee.
    """
    type = kwargs.pop("type","weight")
    uncertainties = kwargs.pop("uncertainties",False)

    measurements = queryset.all()

    quantity = defaultdict(list)
    for meas in measurements:
        for ox in meas.data:
            if type == "molar":
                val = ox.molar_percent
            else:
                val = ox.weight_percent

            if uncertainties:
                # Error is relative
                err = val*ox.error/100
                val = ufloat(val,err)

            # Rescale if normalized
            # (molar should already be rescaled)
            if type == "normalized_weight":
                val *= 100 / meas.oxide_total

            quantity[ox._oxide].append(val)

    # Divide by number of items in queryset
    n = len(measurements)
    output = dict()
    for ox, ls in quantity.items():
        # Mean of values, possibly uncertain
        u = N.mean(ls)

        if hasattr(u,"nominal_value"):
            # Standard deviation of values
            # (from scatter of measurments)
            s = N.std([l.n for l in ls])
            # combine central tendency of distribution,
            # mean of central tendency, and
            # total stdev to get an estimator
            # for the range of the entire distribution
            u = ufloat(u.n,u.s+s)
            # Uncertainties module doesn't include
            # standard deviation of arrays (yet)
            #allclose_uncertain(u.s,unumpy.std(ls))
        output[ox] = u

    # Get out of defaultdict
    return output

@app.with_context
def test_grouped_measurements():
    """
    Test measurement of oxide parameters across
    several types of quantity (molar, weight,
    normalized weight) to make sure that
    queryset implementation corresponds to
    naiive (slow) implementation.
    """
    types = ["molar","weight","normalized_weight"]

    # Pick an arbitrary queryset
    queryset = ProbeMeasurement.query.filter(ProbeMeasurement.id <= 100)

    for t in types:
        print(t)
        kwargs = dict(type=t,uncertainties=True)
        comp = average_composition(queryset, **kwargs)
        naive_comp = naive_composition(queryset, **kwargs)

        if t != "weight":
            for i in (comp,naive_comp):
                s = sum(i.values()).n
                assert N.allclose(s,100)

        for k,quantity in comp.items():
            print(k, quantity, naive_comp[k])
            assert allclose_uncertain(quantity, naive_comp[k], rtol=0.05)

def test_sql_norm():
    """
    Test normalization of data in SQL
    """
    filt = ProbeDatum.measurement_id == 1

    f = ProbeDatum.weight_percent*100 /ProbeMeasurement.oxide_total

    with app.app_context():
        q1 = db.session.query(ProbeDatum)\
            .join(ProbeMeasurement)\
            .filter(filt)\
            .with_entities(f)\

        d = [a[0] for a in q1.all()]
        print(sum(d))
        assert sum(d) == 100
