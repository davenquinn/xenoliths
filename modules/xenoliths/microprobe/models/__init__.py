from __future__ import division

import operator
import periodictable as pt
from uncertainties import ufloat
from sqlalchemy.dialects.postgresql import JSON
from geoalchemy2.types import Geometry
from slugify import slugify

from ..converter import Converter
from ..quality import compute_mineral, data_quality
from ...config import MINERALS, MINERAL_SYSTEMS
from ...core.models.base import BaseModel, db
from ...database.util import ChoiceType
from .serialize import serialize

tags = db.Table('tag_manager',
    db.Column('tag_name', db.String(64), db.ForeignKey('tag.name')),
    db.Column('page_id', db.Integer, db.ForeignKey('point.id'))
)

class Tag(BaseModel):
    name = db.Column(db.String(64), primary_key=True)
    __str__ = lambda self: self.name
    __repr__ = lambda self: "Tag {0}".format(self)

class Point(BaseModel):
    id = db.Column(db.Integer,primary_key=True)
    line_number = db.Column(db.Integer, nullable=False)
    geometry = db.Column(Geometry("Point"))
    mineral = db.Column(ChoiceType(MINERALS))

    oxides = db.Column(JSON)
    errors = db.Column(JSON)
    transforms = db.Column(JSON)
    molar = db.Column(JSON)
    formula = db.Column(JSON)
    params = db.Column(JSON)

    sample_id = db.Column(
        db.String,
        db.ForeignKey('sample.id'),
        nullable=True)

    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('points', lazy='dynamic'))
    # Object methods
    serialize = serialize

    def __repr__(self):
        return "Probe analysis {0}:{1} {2}".format(
            self.sample_id,
            self.line_number,
            self.mineral)

    @property # for compatibility
    def n(self):
        return self.line_number

    def add_tag(self,name):
        slug = slugify(name.strip(), to_lower=True)
        tag = Tag.get_or_create(name=slug)
        try:
            idx = self.tags.index(tag)
        except ValueError:
            self.tags.append(tag)
        return tag.name

    def remove_tag(self,name):
        tag = Tag.query.get(name)
        try:
            self.tags.remove(tag)
        except ValueError:
            pass

    def derived_data(self):
        self.molar = self.compute_molar()
        self.transforms = {k: self.compute_transform(k) for k in MINERAL_SYSTEMS.keys()}
        self.compute_params()
        data_quality(self, False)

    def compute_molar(self):
        """Computes the molar percentage of KNOWN products
        (i.e. unknown components not included)."""
        molar = {}
        for key, value in self.oxides.items():
            if key == 'Total': continue
            oxide = pt.formula(key)
            molar[key] = value/oxide.mass
        total = sum(molar.itervalues())
        for key, value in molar.iteritems():
            molar[key] = value/total*100
        molar["Total"] = 100
        return molar

    def compute_ratio(self, top, bottom):
        molar = self.molar
        if 0 in (molar[top],molar[bottom]):
            return None
        else:
            return 100*molar[top]/(molar[top]+molar[bottom])

    def compute_params(self):
        molar = self.molar
        params = {
            "Mg#": self.compute_ratio("MgO","FeO"),
            "Cr#": self.compute_ratio("Cr2O3","Al2O3")
        }
        self.params = params
        return params

    def compute_transform(self, system="pyroxene"):
        converter = Converter(system)
        return converter.transform(self.molar)

    def __get_atomic__(self):
        formula = {}
        for key, molar_pct in self.molar.items():
            if key == "Total": continue
            oxide = pt.formula(key)
            for i,n in oxide.atoms.iteritems():
                formula[str(i)] = formula.get(str(i),0)+n*molar_pct
        return formula

    def get_cations(self, oxygen=6, uncertainties=True):
        formula = self.__get_atomic__()
        scalar = oxygen/formula["O"]
        for key, value in formula.iteritems():
            formula[key] = value*scalar
        del formula["O"]

        if uncertainties and self.errors:
            for key, cation in formula.iteritems():
                err_pct = self.errors[key]
                abs_err = err_pct/100.*cation
                formula[key] = ufloat(cation, abs_err, key+"_probe")

        formula["Total"] = sum(formula.itervalues())
        return formula

    def compute_formula(self, oxygen=6):
        formula = self.__get_atomic__()
        scalar = oxygen/formula["O"]
        for key, value in formula.iteritems():
            formula[key] = value*scalar
        formula["Total"] = sum(formula.itervalues())
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
            print obj.id, dif
