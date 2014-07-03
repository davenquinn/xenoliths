from __future__ import division

from sqlalchemy.dialects.postgresql import ARRAY

from ...application import db

class Sample(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    desc = db.Column(db.Text)
    classification = db.Column(ARRAY(db.Integer, dimensions=2))

    point = db.relationship("Point", backref="sample")
