from __future__ import division
from sqlalchemy import func

from .thermometers import BKN, Taylor1998
from .barometers import Ca_Olivine
from .results import pyroxene_pairs, closest
from ..models import ProbeMeasurement,Sample
from ..application import db
from ..microprobe.models.query import tagged, exclude_bad

def triplets(queryset, distinct=None):
    olivines = queryset.filter(
            ProbeMeasurement.mineral=='ol')
    for ol in olivines.all():
        # Get closest clinopyroxene
        opx = (queryset
            .filter(ProbeMeasurement.mineral=='opx')
            .order_by(ProbeMeasurement.geometry.ST_Distance(ol.geometry))
            .first())
        cpx = (queryset
            .filter(ProbeMeasurement.mineral=='cpx')
            .order_by(ProbeMeasurement.geometry.ST_Distance(ol.geometry))
            .first())
        print opx, cpx, ol
        yield opx,cpx,ol

def geobaric_gradient(depth):
    return depth*.03 #GPa/km

class GeoThermometryResult(object):
    pressure_basis = 1.5
    def __init__(self,opx, cpx, ol=None):
        #assert opx.sample == cpx.sample
        self.sample = opx.sample
        self.opx = opx
        self.cpx = cpx
        self.ol = ol

        self.temperature = Taylor1998(opx,cpx).temperature(pressure=self.pressure_basis)
        self.bkn = BKN(opx,cpx).temperature(pressure=self.pressure_basis)
        self.pressure = Ca_Olivine(ol,cpx).pressure(self.bkn)
        self.depth = self.pressure/.03

    # def grouped_pressure(self):
        # if self.all_olivines is None:
            # all_olivines = ProbeMeasurement.query.filter(
                    # ProbeMeasurement.mineral=="ol",
                    # ProbeMeasurement.sample==self.sample)
            # all_olivines = exclude_bad(tagged(all_olivines,"core"))
            # self.all_olivines = all_olivines
        # return Ca_Olivine(self.all_olivines,self.cpx).pressure(self.bkn)

def pressure_measurements(single=False,core=True):
    base_queryset = exclude_bad(ProbeMeasurement.query)
    if core:
        base_queryset = tagged(base_queryset,"core")
    for sample in Sample.query.filter_by(xenolith=True):
        queryset = base_queryset.filter(ProbeMeasurement.sample==sample)
        if single:
            minerals = ('opx','cpx','ol')
            res = tuple(queryset
                    .filter(ProbeMeasurement.mineral==i)
                    for i in minerals)
            res = GeoThermometryResult(*res)
            res.sample = sample
            yield res
        else:

            for grains in list(triplets(queryset)):
                res = GeoThermometryResult(*grains)
                #res.all_olivines = all_olivines
                yield res
