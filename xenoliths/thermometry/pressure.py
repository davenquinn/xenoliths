from __future__ import division, print_function
from sqlalchemy import func
from itertools import product
from click import progressbar
import numpy as N

from .thermometers import BKN, Taylor1998
from .barometers import Ca_Olivine
from .results import pyroxene_pairs, closest
from ..models import ProbeMeasurement,Sample
from ..application import db
from ..microprobe.group import get_cations
from ..microprobe.models.query import tagged, exclude_bad

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

def geobaric_gradient(depth):
    return depth*.03 #GPa/km

class GeoThermometryResult(object):
    init_pressure_basis = 1.5
    def __init__(self,opx, cpx, ol=None, **kwargs):
        #assert opx.sample == cpx.sample
        self.opx = opx
        self.cpx = cpx
        self.ol = ol

        self.temperature = Taylor1998(opx,cpx, **kwargs).temperature(pressure=self.init_pressure_basis)

        bkn = BKN(opx,cpx, **kwargs)
        barometer = Ca_Olivine(ol,cpx, bkn, **kwargs)
        self.pressure = barometer()
        self.bkn = bkn.temperature(pressure=self.pressure)
        self.depth = self.pressure/.03

def mineral_data(queryset, mineral='opx',**kwargs):
    mn = ProbeMeasurement.mineral==mineral
    qs = queryset.filter(mn)
    kw = dict(
        uncertainties=False,
        oxygen=6 if mineral != 'ol' else 4)
    return [get_cations(c,**kw) for c in qs.all()]

def pressure_measurements(core=True, all_possible=False,**kwargs):
    base_queryset = exclude_bad(ProbeMeasurement.query)
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

