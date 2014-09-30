from __future__ import division
from .thermometers import BKN, Taylor1998
from .barometers import Ca_Olivine
from .results import pyroxene_pairs, closest
from ..models import ProbeMeasurement,Sample
from ..microprobe.models.query import tagged, exclude_bad

def triplets(queryset):
    olivines = queryset.filter(ProbeMeasurement.mineral=="ol")
    for opx,cpx in pyroxene_pairs(queryset):
        yield opx,cpx,closest(olivines, cpx)

def geobaric_gradient(depth):
    return depth*.03 #GPa/km

class GeoThermometryResult(object):
    pressure_basis = 1.5
    def __init__(self,opx, cpx, ol=None):
        assert opx.sample == cpx.sample
        self.sample = opx.sample
        self.opx = opx
        self.cpx = cpx

        self.temperature = Taylor1998(opx,cpx).temperature(pressure=self.pressure_basis)
        self.bkn = BKN(opx,cpx).temperature(pressure=self.pressure_basis)
        self.pressure = Ca_Olivine(ol,cpx).pressure(self.bkn)

    def grouped_pressure(self):
        all_olivines = ProbeMeasurement.query.filter(
                ProbeMeasurement.mineral=="ol",
                ProbeMeasurement.sample==self.sample)
        all_olivines = exclude_bad(tagged(all_olivines,"core"))
        return Ca_Olivine(all_olivines.all(),self.cpx).pressure(self.bkn)

    @property
    def depth(self):
        return self.grouped_pressure()/.03


def pressure_measurements():
    base_queryset = tagged(exclude_bad(ProbeMeasurement.query),"core")
    for sample in Sample.query.all():
        queryset = base_queryset.filter(ProbeMeasurement.sample==sample)
        for grains in triplets(queryset):
            yield GeoThermometryResult(*grains)
