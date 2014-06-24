from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet

bad_tags = [
    "bad",
    "alteration",
    "mixed",
    "marginal",
    "anomalous",
    "review",
    "near alteration",
    "high-ti"
]

class PointQuerySet(GeoQuerySet):

    def get_oxides(self, oxygen=6, uncertainties=True):
        nobs = len(self)
        formula = {}
        for obj in self:
            oxs = obj.oxides
            for i,n in oxs.iteritems():
                formula[i] = formula.get(i,0)+n

        for key, item in formula.iteritems():
            formula[key] = item/nobs

        return formula

    def get_cations(self, oxygen=6, uncertainties=True):
        nobs = len(self)
        formula = {}
        for obj in self:
            cats = obj.get_cations(oxygen, uncertainties=uncertainties)
            for i,n in cats.iteritems():
                formula[i] = formula.get(i,0)+n

        for key, item in formula.iteritems():
            formula[key] = item/nobs

        return formula

    def remove_bad(self):
        return self.exclude(tags__name__in=bad_tags)

class PointManager(models.Manager):
    def get_query_set(self):
        return PointQuerySet(self.model)
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)