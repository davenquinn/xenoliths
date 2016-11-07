from __future__ import division, print_function
from PIL import Image
import click
from click import echo, style

from ...application import app, db
from pathlib import Path
from ...core.models import Sample
from ..models import ProbeImage, ProbeSession
from .util import model_factory, find_date

def get_info(info_filename):
    with open(str(info_filename)) as f:
        for line in f:
            if line.isspace(): continue
            data = tuple(i.strip()\
                for i in line.split("="))
            yield data

def sanitize_name(name):
    pairs = [(" ","_"),("(",""),(")","")]
    for p in pairs:
        name = name.replace(*p)
    if len(name) > 255:
        name = name[:255]
    return name

field_map = dict(
    magnification='Magnification',
    x_min='Stage Xmin',
    x_max='Stage Xmax',
    y_min='Stage Ymin',
    y_max='Stage Ymax')

find_image = model_factory(ProbeImage, echo=True)
find_session = model_factory(ProbeSession, echo=True)

def import_image(sample, image, info_file):
    info = {k:v for k,v in get_info(info_file)}
    name = sanitize_name(image.stem)

    s1 = image.stem.replace("_","-")
    session = find_session(
        sample_id=sample.id,
        date=find_date(s1))

    data = {k:float(info[v])\
        for k,v in field_map.items()}
    data["sample_id"] = sample.id
    data["session_id"] = session.id

    model = find_image(name=name)
    for k,d in data.items():
        setattr(model,k,d)

    # Save files if they don't already exist
    try:
        assert model.path.is_file()
    except AssertionError:
        im = Image.open(str(image))
        im.save(str(model.path))

@click.command()
def import_images():
    """ Imports probe images into the database.
    """
    basepath = Path(app.config.get("RAW_DATA"))/"Probe"/"images"

    for d in basepath.iterdir():
        if not d.is_dir(): continue
        sample = db.session.query(Sample).get(d.name)
        for image in d.glob("*.bmp"):
            info = image.with_suffix(".txt")
            if not info.is_file():
                echo(style(image.name, fg="green")\
                    +" has no associated information file")
                echo("...."+style("skipping",fg="red"))
                continue
            import_image(sample, image, info)
    db.session.commit()
