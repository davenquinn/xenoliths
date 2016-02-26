# =*= coding:utf-8 =*=

from periodictable import elements
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.ext.hybrid import hybrid_property
from uncertainties import ufloat
from collections import defaultdict

from ..core.models.base import BaseModel, db
from ..database.util import ChoiceType
from ..config import MINERALS

class SIMSDatum(BaseModel):
    __tablename__ = "sims_datum"
    measurement_id = db.Column(
        db.Integer,
        db.ForeignKey('sims_measurement.id'),
        primary_key=True)
    _element = db.Column("element", db.Integer, primary_key=True)
    norm_ppm = db.Column(db.Float)
    norm_std = db.Column(db.Float)
    raw_ppm = db.Column(db.Float)
    raw_std = db.Column(db.Float)
    bad = db.Column(db.Boolean, default=False)

    @hybrid_property
    def norm(self):
        return self.__ufloat__("norm")
    @norm.expression
    def norm(cls):
        return array([cls.norm_ppm, cls.norm_std])

    @hybrid_property
    def raw(self):
        return self.__ufloat__("norm")
    @raw.expression
    def raw(cls):
        return array([cls.raw_ppm, cls.raw_std])

    def __ufloat__(self, t="norm"):
        ppm = getattr(self, t+"_ppm")
        std = getattr(self, t+"_std")
        if std < 0: std = 0
        return ufloat(ppm,std)

    def __repr__(self):
        n = self.norm
        return "{0}: {1}±{2}".format(self.element,n.n,n.s)

    @hybrid_property
    def element(self):
        return elements[self._element]
    @element.expression
    def element(cls):
        return cls._element

    @element.setter
    def element(self, value):
        self._element = getattr(elements,value).number

class SIMSMeasurement(BaseModel):
    __tablename__ = "sims_measurement"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    sample_id = db.Column(
        db.String(64),
        db.ForeignKey("sample.id"))
    description = db.Column(db.String(1024))
    mineral = db.Column(db.String)

    data = db.relationship(SIMSDatum,
        backref="measurement",
        order_by=SIMSDatum._element)
    sample = db.relationship("Sample", backref="sims_measurements")

    def __repr__(self):
        return "SIMS: {0} {1} ({2})".format(
            self.sample.id, self.name, self.mineral)

def average(queryset, uncertainties=True, normalized=True):
    attr = "norm" if normalized else "raw"
    if not uncertainties: attr += "_ppm"
    length = queryset.count()
    def reactor(d, n):
        for e in n.data:
            if e.bad: continue
            d[e.element.symbol] += getattr(e,attr)/length
        return d
    data = reduce(reactor, queryset.all(), defaultdict(float))
    return defaultdict(lambda: float("NaN"), data)
