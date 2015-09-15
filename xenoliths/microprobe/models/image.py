from pathlib import Path
from ...application import app
from ...core.models import BaseModel, db
from sqlalchemy.ext.hybrid import hybrid_property

class ProbeImage(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    x_min = db.Column(db.Float)
    x_max = db.Column(db.Float)
    y_min = db.Column(db.Float)
    y_max = db.Column(db.Float)
    magnification = db.Column(db.Float)

    sample_id = db.Column(
        db.String,
        db.ForeignKey('sample.id'),
        nullable=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey('probe_session.id'))

    filename = property(lambda s: s.name+".png")

    @property
    def path(self):
        p = Path(app.config.get("DATA_DIR"))/"probe-images"
        return p/self.filename

    @property
    def url(self):
        return "/data/probe-images/"+self.filename

    def serialize(self):
        return dict(
            sample=self.sample_id,
            url=self.url,
            bbox=[[self.x_min,self.y_min],
                  [self.x_max,self.y_max]])

