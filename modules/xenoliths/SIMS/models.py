class Datum():
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

class Measurement(object):
    __tablename__ = "sims_measurement"
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(
        db.String(64),
        db.ForeignKey("sample"))
    description = db.Column(db.String(256))
    mineral = db.Column(db.String(256))

    elements = db.relationship("sims_datum",
        backref="measurement",
        order_by="sims_datum.element")
    sample = db.relationship("sample", backref="sims_measurements")
