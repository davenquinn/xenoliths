from ..core.models.base import BaseModel, db
from ..database.util import ChoiceType
from ..config import MINERALS

class Datum(BaseModel):
    __tablename__ = "sims_datum"
    measurement_id = db.Column(
        db.Integer,
        db.ForeignKey('sims_measurement.id'),
        primary_key=True)
    element = db.Column(db.Integer, primary_key=True)
    norm_ppm = db.Column(db.Float)
    norm_std = db.Column(db.Float)
    raw_ppm = db.Column(db.Float)
    raw_std = db.Column(db.Float)

class Measurement(BaseModel):
    __tablename__ = "sims_measurement"
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(
        db.String(64),
        db.ForeignKey("sample.id"))
    description = db.Column(db.String(1024))
    mineral = db.Column(ChoiceType(MINERALS))

    elements = db.relationship("sims_datum",
        backref="measurement",
        order_by="sims_datum.element")
    sample = db.relationship("sample", backref="sims_measurements")
