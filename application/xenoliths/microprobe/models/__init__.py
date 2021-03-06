

import operator
import periodictable as pt
from periodictable import elements
from uncertainties import ufloat
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import BaseQuery
from geoalchemy2.types import Geometry
from slugify import slugify
from collections import defaultdict

from .image import ProbeImage
from ..converter import Converter
from .compute import oxygen_basis, compute_mineral
from ...config import OXIDES, MINERALS, MINERAL_SYSTEMS
from ...core.models import BaseModel, db

FORMULAE = {k:pt.formula(k) for k in OXIDES}

tags = db.Table('tag_manager',
    db.Column('tag_name', db.String(64), db.ForeignKey('tag.name')),
    db.Column('page_id', db.Integer, db.ForeignKey('probe_measurement.id')))

class Tag(BaseModel):
    name = db.Column(db.String(64), primary_key=True)
    __str__ = lambda self: self.name
    __repr__ = lambda self: "Tag {0}".format(self)

class ProbeSession(BaseModel):
    __tablename__ = "probe_session"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    sample_id = db.Column(
        db.String,
        db.ForeignKey('sample.id'))

    translate_x = db.Column(db.Float, default=0)
    translate_y = db.Column(db.Float, default=0)
    rotate = db.Column(db.Float, default=0)

    sample = db.relationship('Sample',
        backref=db.backref("sessions"))

class ProbeDatum(BaseModel):
    __tablename__ = "probe_datum"
    measurement_id = db.Column(
        db.Integer,
        db.ForeignKey('probe_measurement.id'),
        primary_key=True)
    _cation = db.Column("cation",db.Integer, primary_key=True)
    _oxide = db.Column("oxide",db.String(5),nullable=False)
    weight_percent = db.Column(db.Float)
    molar_percent = db.Column(db.Float)
    error = db.Column(db.Float)

    def __repr__(self):
        return "{0}: {1}%wt".format(self.oxide,self.weight_percent)

    @hybrid_property
    def cation(self):
        return elements[self._cation]

    @cation.setter
    def cation(self, value):
        self._cation = getattr(elements,value).number

    @hybrid_property
    def oxide(self):
        return FORMULAE[self._oxide]

    @oxide.setter
    def oxide(self, value):
        self._oxide = value

class QueryClass(BaseQuery):
    from .query import tagged, exclude_bad

class ProbeMeasurement(BaseModel):
    __tablename__ = "probe_measurement"
    query_class = QueryClass

    id = db.Column(db.Integer,primary_key=True)
    line_number = db.Column(db.Integer, nullable=False)
    geometry = db.Column(Geometry("Point"))
    location = db.Column(Geometry("Point"))
    mineral = db.Column(db.String)

    oxide_total = db.Column(db.Float)
    mg_number = db.Column(db.Float)
    cr_number = db.Column(db.Float)
    spot_size = db.Column(db.Float)

    errors = db.Column(JSON)
    transforms = db.Column(JSON)
    formula = db.Column(JSON)
    params = db.Column(JSON)

    sample_id = db.Column(
        db.String,
        db.ForeignKey('sample.id'),
        nullable=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey('probe_session.id'))

    data = db.relationship('ProbeDatum',
        backref=db.backref("measurement"),
        lazy="joined")
    data_query = db.relationship(ProbeDatum, lazy="dynamic")

    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('points', lazy='dynamic'),
        lazy="joined")

    session = db.relationship('ProbeSession',
        backref=db.backref("measurements"))

    # Object methods
    from .serialize import serialize
    from .compute import compute_derived

    def oxide(self, oxide):
        """ Gets the probe datum corresponding to a specific oxide"""
        return self.data_query.filter_by(_oxide=oxide).first()

    def __repr__(self):
        return "Probe analysis {0}:{1} {2}".format(
            self.sample_id,
            self.line_number,
            self.mineral_name)

    @property # for compatibility
    def n(self):
        return self.line_number

    @property
    def oxygen_basis(self):
        return oxygen_basis(self.mineral)

    @property
    def mineral_name(self):
        try:
            return MINERALS[self.mineral]
        except KeyError:
            return "Unknown"

    def add_tag(self,name):
        slug = slugify(str(name.strip()))
        tag = Tag.get_or_create(name=slug)
        try:
            idx = self.tags.index(tag)
        except ValueError:
            self.tags.append(tag)
        db.session.flush()
        return tag.name

    def remove_tag(self,name):
        tag = Tag.query.get(name)
        try:
            self.tags.remove(tag)
        except ValueError:
            pass

    def __get_atomic__(self, uncertainties=True):
        formula = defaultdict(int)
        for d in self.data:
            for i, n in d.oxide.atoms.items():
                v = n*d.molar_percent
                if uncertainties:
                    v = ufloat(v,v*d.error)
                formula[str(i)] += v
        return formula

    def get_cations(self, oxygen=6, uncertainties=True):
        formula = self.__get_atomic__(uncertainties)
        scalar = oxygen/formula["O"]
        for key, value in formula.items():
            formula[key] = value*scalar
        del formula["O"]

        formula["Total"] = sum(formula.values())
        return formula

def test_formula():
    """Tests the calculation of oxide percents."""
    query = Point.objects.all()
    for obj in query:
        a = 0
        for cat in settings.CATIONS:
            a += getattr(obj,cat)
        a += obj.O
        dif = a-obj.Total
        if fabs(dif) > .0001:
            print(obj.id, dif)
