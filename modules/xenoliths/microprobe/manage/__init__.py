import click
from click import echo
import os
from geoalchemy2.elements import WKTElement
import json
import numpy as N
from flask.ext.script import Manager

from .util import model_factory, find_spot_size
from .file_handler import get_data
from .images import import_images
from ...application import app, db
from ...core.models import Sample
from ..models import ProbeMeasurement, ProbeDatum, ProbeSession

ProbeCommand = click.Group(help="Command to manage microprobe data")
ProbeCommand.add_command(import_images, name="import-images")

find_datum = model_factory(ProbeDatum)
find_sample = model_factory(Sample, echo=True)
find_session = model_factory(ProbeSession, echo=True)
find_measurement = model_factory(ProbeMeasurement, echo=True)

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

def create_data(point,row):
    """ Imports data from rows into a probe datum for each cation.
    """
    parts = tuple(app.config.get(i) for i in ("CATIONS", "OXIDES"))
    for cation,oxide in zip(*parts):
        try:
            wt_pct = row[oxide]
        except KeyError:
            continue
        if N.isnan(wt_pct):
            continue

        d = find_datum(
            measurement=point,
            _oxide=oxide)
        d.cation = cation
        d.weight_percent = row[oxide]
        d.error = row[d.cation.symbol+" %ERR"]
        yield d

def import_measurement(row):
    point = find_measurement(
        line_number = row["LINE"],
        sample = find_sample(id=row["sample_id"]),
        session = find_session(
            sample_id=row["sample_id"],
            date=row["date"]))

    point.location = WKTElement("POINT({x} {y})".format(
        x = row["X-POS"],
        y = row["Y-POS"]))
    point.geometry = geometry(row)
    point.spot_size = find_spot_size(row["SAMPLE"])

    ls = [o.weight_percent for o in create_data(point,row)]
    oxide_total = sum(ls)
    try:
        assert N.abs(row["TOTAL"] - oxide_total) < 0.001
    except AssertionError:
        print("ERROR: Totals do not match up!")
    point.oxide_total = oxide_total
    point.compute_derived()

@ProbeCommand.command(name="import")
def setup():
    """Imports microprobe data."""
    data = get_data(app.config.get("RAW_DATA"))
    rows = (row for (i,row) in data.iterrows())
    n = len(data.index)

    echo("Importing probe measurements...")
    with click.progressbar(rows, length=n) as bar:
        for row in bar:
            import_measurement(row)

    db.session.commit()
    write_json()

def recalculate():
    """Calculates derived parameters for already-imported data"""
    for meas in ProbeMeasurement.query.all():
        print(meas.id)
        meas.compute_derived(db.session)
    db.session.commit()

ProbeCommand.add_command(recalculate, name="recalculate")
