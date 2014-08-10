from __future__ import division

from sqlalchemy.dialects.postgresql import ARRAY

from .base import BaseModel,db

class Sample(BaseModel):
    id = db.Column(db.String(64), primary_key=True)
    desc = db.Column(db.Text)
    classification = db.Column(ARRAY(db.String(8), dimensions=2))

    point = db.relationship("Point", backref="sample")

    def __repr__(self):
        return "Sample {0}".format(self.id)
