import click
from click import echo
import os
from geoalchemy2.elements import WKTElement
import json
import numpy as N
from flask.ext.script import Manager

from .file_handler import get_data
from .images import import_images
from ...application import app, db
from ...core.models import Sample
from ..models import ProbeMeasurement, ProbeDatum

ProbeCommand = click.Group(help="Command to manage microprobe data")
ProbeCommand.add_command(import_images, name="import-images")

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
    xy = row["X-POS_affine"],row["Y-POS_affine"]
    return WKTElement("POINT({0} {1})".format(*xy))

def create_samples(data):
    for val in data["sample_id"].unique():
        sample = Sample.get_or_create(id=val)
        db.session.add(sample)
        yield val, sample
    db.session.commit()

def create_sessions(data):
    pass

def create_data(point,row):
    for oxide in app.config.get("OXIDES"):
        d = ProbeDatum.get_or_create(
            measurement=point,
            _oxide=oxide)
        d.cation = oxide[0:2]
        d.weight_percent = row[oxide]
        d.error = row[d.cation.symbol+" %ERR"]
        db.session.add(d)
        yield d

@ProbeCommand.command(name="import")
def setup():
    """Imports microprobe data."""
    data = get_data(app.config.get("RAW_DATA"))

    samples = {k:v for k,v in create_samples(data)}

    for i,row in data.iterrows():
        print(i)
        sample = samples[row["sample_id"]]
        point = ProbeMeasurement.get_or_create(
            line_number=row["LINE"],
            sample=sample)
        point.location = WKTElement("POINT({x} {y})".format(
            x = row["X-POS"],
            y = row["Y-POS"]))
        point.geometry = geometry(row)

        oxide_total = sum([o.weight_percent for o in create_data(point,row)])
        assert N.abs(row["TOTAL"] - oxide_total) < 0.001
        point.oxide_total = oxide_total

        db.session.add(point)
        db.session.commit()

    recalculate()
    write_json()

@ProbeCommand.command()
def recalculate():
    """Calculates derived parameters for already-imported data"""
    for meas in ProbeMeasurement.query.all():
        print(meas.id)
        meas.compute_derived(db.session)
    db.session.commit()

