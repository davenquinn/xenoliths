from __future__ import print_function, division

from sqlalchemy.sql import func
from uncertainties import ufloat, umath
from uncertainties.unumpy import uarray
import numpy as N

def test_oxides():
    from ..application import app, db, ProbeMeasurement
    with app.app_context():
        from .group import get_oxides
        data = get_oxides(ProbeMeasurement.query, uncertainties=False)
        s = sum(data.values())
        d = db.session.query(func.sum(ProbeMeasurement.oxide_total)\
                /func.count("*")).all()
        print(s,d)
        assert N.allclose(s, d)

def test_molar():
    """
    Tests that molar percentages always sum to 100
    """
    from ..application import app, ProbeMeasurement
    with app.app_context():
        from .group import get_molar
        queryset = ProbeMeasurement.query\
            .filter(ProbeMeasurement.sample_id == "CK-4")\
            .filter(ProbeMeasurement.mineral == "opx")
        data = get_molar(queryset, uncertainties=False)
        s = sum(data.values())
        print(s)
        assert N.allclose(s, 100)

def test_cations():
    """ Tests that cation proportions computed using SQL
        are functionally the same as iteratively computed
        values.
    """
    from ..application import app, ProbeMeasurement
    with app.app_context():
        from .group import get_cations, iterate_cations

        queryset = ProbeMeasurement.query\
            .filter(ProbeMeasurement.id < 100)
        g = get_cations(queryset, uncertainties=True)
        d = iterate_cations(queryset, uncertainties=True)
        for k in g.keys():
            print(k, g[k], d[k])
            assert abs(g[k].n - d[k].n) <= 0.5*g[k]
            assert abs(g[k].n - d[k].n) <= 0.1
            assert 1/2 < g[k].s/d[k].s < 2

def test_uncertainties():
    """ Tests the method used to calculate uncertainties in
        SQL
        Note: this tests uncertainties on the calculation of
        the mean itself!
    """
    n = 100
    arr = N.random.randn(2,n)
    arr[1] = 0.1*N.abs(arr[1])
    unc = N.array([ufloat(*tuple(i)) for i in arr.T])
    avg = N.mean(unc)

    k = arr[0].mean()
    s = N.sqrt(N.sum(arr[1]**2))/n
    avg2 = ufloat(k,s)
    print(avg,avg2)
    assert N.allclose(avg.n,avg2.n)
    assert N.allclose(avg.s, avg2.s)

def test_uncertainties_2():
    """ Tests the method used to calculate uncertainties in
        SQL
        Note: this tests uncertainties in the calculation of
        a single measured value
    """
    n = 100
    arr = N.random.randn(2,n)
    arr[1] = 0.1*N.abs(arr[1])
    #unc = N.array([ufloat(*tuple(i)) for i in arr.T])
    unc = uarray(arr[0],arr[1])
    mean = unc.mean()
    variance = N.mean((unc-mean)**2)
    avg = ufloat(unc.mean().n, umath.sqrt(variance).n)

    k = arr[0].mean()
    s = N.sqrt(N.sum(arr[1]**2))/n
    avg2 = ufloat(k,s)
    print(avg,avg2)
    assert N.allclose(avg.n,avg2.n)
    assert N.allclose(avg.s, avg2.s)
