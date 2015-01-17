import click
from click import echo
from pathlib import Path

import numpy as N

from ..models import Sample
from .models import SIMSMeasurement, SIMSDatum, db
from ..application import app
from .quality import check_quality

SIMSCommand = click.Group(help="Command to manage SIMS data")

def load_data(file):
    dtype = [("el", str, 2), ("abundance", float), ("err", float)]
    return N.loadtxt(str(file), skiprows=2, dtype=dtype)

def import_measurement(mineral, raw,norm):
    def clean_filename(name):
        """ Returns sample id and cleaned name from measurement"""
        sid, end = tuple(raw.stem.split("_",1))
        return sid, end.split(".")[0]

    assert raw.stem == norm.stem
    sample_id, name = clean_filename(raw.stem)
    sample = Sample.query.get(sample_id)
    if not sample: return # We're not importing standards
    meas = SIMSMeasurement(
        name = name,
        sample = sample,
        mineral = app.config["MINERALS"][mineral])
    echo(meas)
    db.session.add(meas)

    raw, norm = tuple(map(load_data,(raw,norm)))
    for rd, nd in zip(raw, norm):
        assert rd["el"] == nd["el"]
        d = SIMSDatum(
            measurement = meas,
            raw_ppm = rd["abundance"],
            raw_std = rd["err"],
            norm_ppm = nd["abundance"],
            norm_std = nd["err"])
        d.element = rd["el"]
        db.session.add(d)


SIMSCommand.add_command(check_quality)

@SIMSCommand.command()
def init():
    """ Import SIMS data into application."""
    SIMSDatum.query.delete()
    SIMSMeasurement.query.delete()
    db.session.commit()

    data_dir = Path(app.config.get("RAW_DATA"))/"SIMS"
    for mineral in ["cpx", "opx"]:
        directory = data_dir/mineral
        raw = list(directory.glob("*.ppm"))
        nrm = list(directory.glob("*.nrm"))
        [import_measurement(mineral,*i) for i in zip(raw,nrm)]
        db.session.commit()
