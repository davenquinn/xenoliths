from __future__ import division, print_function
from sqlalchemy import func
from itertools import product
from click import progressbar
import numpy as N
from geotherm.units import u
from heatflow.config import (
    continental_crust,
    oceanic_mantle, interface_depth)

from .thermometers import BKN, Taylor1998, Ca_OPX_Corr, Ca_OPX
from .barometers import Ca_Olivine, bkn_to_ta98
from .results import pyroxene_pairs, closest
from ..models import ProbeMeasurement,Sample
from ..application import db
from ..microprobe.group import get_cations
from ..microprobe.models.query import tagged, exclude_bad, exclude_tagged

def triplets(queryset, distinct=None, all_possible=False, limit=1):
    olivines = queryset.filter(
            ProbeMeasurement.mineral=='ol')
    for ol in olivines.all():
        # Get closest clinopyroxene
        opx = (queryset
            .filter(ProbeMeasurement.mineral=='opx')
            .order_by(ProbeMeasurement.geometry.ST_Distance(ol.geometry))
            .limit(limit))
        cpx = (queryset
            .filter(ProbeMeasurement.mineral=='cpx')
            .order_by(ProbeMeasurement.geometry.ST_Distance(ol.geometry))
            .limit(limit))
        for o,c in zip(opx,cpx):
            yield o,c,ol

def simple_geobaric_gradient(depth):
    return depth/.03 #GPa/km

def geobaric_gradient(pressure):
    rho0 = continental_crust.density
    g = u(9.8,'m/s^2')
    P = u(pressure,'GPa')
    rho1 = oceanic_mantle.density
    d0 = interface_depth

    a0 = P/g/rho0
    if a0 < d0:
        return a0.into('km')

    a = P/g - rho0*d0 + rho1*d0
    a/=rho1
    return a.into('km')

class GeoThermometryResult(object):
    init_pressure_basis = 1.5
    def __init__(self,opx, cpx, ol=None, **kwargs):
        #assert opx.sample == cpx.sample
        self.opx = opx
        self.cpx = cpx
        self.ol = ol

        ta98 = Taylor1998(opx,cpx, **kwargs)
        ta98.uncertainties = True

        self.init_temperature = ta98.temperature(pressure=self.init_pressure_basis)

        thermometer = BKN(opx,cpx, uncertainties=True)
        barometer = Ca_Olivine(ol,cpx,thermometer, **kwargs)
        self.pressure,self.bkn = barometer(iterative=True)
        # Map BKN to TA98 for consistency
        self.temperature = bkn_to_ta98(self.bkn)
        try:
            self.depth = geobaric_gradient(self.pressure)
        except ValueError:
            self.depth = N.array([geobaric_gradient(i)
                for i in self.pressure])

def mineral_data(queryset, mineral='opx',**kwargs):
    mn = ProbeMeasurement.mineral==mineral
    qs = queryset.filter(mn)
    kw = dict(
        uncertainties=False,
        oxygen=6 if mineral != 'ol' else 4)
    return [get_cations(c,**kw) for c in qs.all()]

def pressure_measurements(core=True, all_possible=False,**kwargs):
    base_queryset = exclude_bad(ProbeMeasurement.query)

    # Exclude Ca-in-olivine measurements that are higher than clustered data
    base_queryset = exclude_tagged(base_queryset,"high-ca")
    if core:
        base_queryset = tagged(base_queryset,"core")

    n_closest = kwargs.pop('n',1)

    for sample in Sample.query.filter_by(xenolith=True):
        queryset = base_queryset.filter(ProbeMeasurement.sample==sample)
        if all_possible:
            minerals = ('opx','cpx','ol')
            res = tuple(mineral_data(queryset,i) for i in minerals)
            length = N.prod([len(r) for r in res])
            data = product(*res)
        else:
            data = triplets(queryset, limit=n_closest)
            length=None
        print(sample.id,length)
        with progressbar(data,length=length) as bar:
            yield sample, [GeoThermometryResult(*i,**kwargs) for i in bar]

