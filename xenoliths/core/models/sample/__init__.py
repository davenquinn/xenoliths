from flask import current_app
from sqlalchemy.dialects.postgresql import ARRAY

from ..base import BaseModel, db

class Sample(BaseModel):
    id = db.Column(db.String(64), primary_key=True)
    desc = db.Column(db.Text)
    classification = db.Column(ARRAY(db.String(8), dimensions=2))
    xenolith = db.Column(db.Boolean)
    color = db.Column(db.String(64))

    point = db.relationship("ProbeMeasurement", backref="sample")

    from .mineral_modes import modes

    def __repr__(self):
        return "Sample {0}".format(self.id)

