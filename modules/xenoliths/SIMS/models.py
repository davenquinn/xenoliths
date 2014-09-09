from periodictable import elements
from sqlalchemy.ext.hybrid import hybrid_property

from ..core.models.base import BaseModel, db
from ..database.util import ChoiceType
from ..config import MINERALS

class Datum(BaseModel):
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

    @hybrid_property
    def element(self):
        return elements(self._element).symbol

    @element.setter
    def element(self, value):
        self._element = getattr(elements,value).number

class Measurement(BaseModel):
    __tablename__ = "sims_measurement"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    sample_id = db.Column(
        db.String(64),
        db.ForeignKey("sample.id"))
    description = db.Column(db.String(1024))
    mineral = db.Column(ChoiceType(MINERALS))

    data = db.relationship(Datum,
        backref="measurement",
        order_by=Datum._element)
    sample = db.relationship("Sample", backref="sims_measurements")

    def __repr__(self):
        return "SIMS: {0} {1} ({2})".format(
            self.sample.id, self.name, self.mineral)
