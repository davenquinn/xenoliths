from __future__ import division

from flask import current_app
from sqlalchemy.dialects.postgresql import ARRAY

from .base import BaseModel, db

class Sample(BaseModel):
    id = db.Column(db.String(64), primary_key=True)
    desc = db.Column(db.Text)
    classification = db.Column(ARRAY(db.String(8), dimensions=2))

    point = db.relationship("ProbeMeasurement", backref="sample")

    def __repr__(self):
        return "Sample {0}".format(self.id)

    @property
    def color(self):
        return current_app.config.get("COLORS")[self.id]
