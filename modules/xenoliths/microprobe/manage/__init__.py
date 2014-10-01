from click import echo
import os
from geoalchemy2.elements import WKTElement
import json

from .file_handler import get_data
from ...application import app, db
from ...core.models import Sample
from ..models import ProbeMeasurement, ProbeDatum

def write_json():
    path = os.path.join(app.config.get("DATA_DIR"),"data.json")
    data = dict(
        type="FeatureCollection",
        features=map(lambda o: o.serialize(), ProbeMeasurement.query.all()))
    with open(path, "w") as f:
        json.dump(data, f)

def oxide_weights(row):
    ox = {k:row[k] for k in app.config.get("OXIDES")}
    ox["Total"] = sum(ox.values())
    return ox

def geometry(row):
    xy = row["X-POS"],row["Y-POS"]
    return WKTElement("POINT({0} {1})".format(*xy))

def create_samples(data):
    for val in data["sample_id"].unique():
        sample = Sample.get_or_create(id=val)
        db.session.add(sample)
        yield val, sample
    db.session.commit()

def create_data(point,row):
    for oxide in app.config.get("OXIDES"):
        d = ProbeDatum.get_or_create(
            measurement=point,
            oxide=oxide)
        d.cation = oxide[0:2]
        d.oxide_percent = row[oxide]
        d.error = row[d.cation.symbol+" %ERR"]
        db.session.add(d)
        yield d

def import_all():
    data = get_data(app.config.get("RAW_DATA"))

    samples = {k:v for k,v in create_samples(data)}

    for i,row in data.iterrows():
        print(i)
        sample = samples[row["sample_id"]]
        point = ProbeMeasurement.get_or_create(
            line_number=row["LINE"],
            sample=sample)
        point.geometry = geometry(row)
        point.oxide_weight = sum([o.oxide_percent for o in create_data(point,row)])
        db.session.add(point)
        db.session.commit()

    write_json()
