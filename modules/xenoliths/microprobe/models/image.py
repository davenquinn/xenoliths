from ...core.models.base import BaseModel, db
from sqlalchemy.ext.hybrid import hybrid_property
from slugify import Slugify

slug_length = 255
slugify = Slugify(
    to_lower=True,
    max_length=slug_length)

class ProbeImage(BaseModel):
    slug = db.Column(db.String(slug_length))

    xmin = db.Column(db.Float)
    xmax = db.Column(db.Float)
    ymin = db.Column(db.Float)
    ymax = db.Column(db.Float)
    magnification = db.Column(db.Float)

    sample_id = db.Column(
        db.String,
        db.ForeignKey('sample.id'),
        nullable=True)

    @hybrid_property
    def name(self):
        return self.slug

    @name.setter
    def name(self, value):
        self.slug = slugify(value)
