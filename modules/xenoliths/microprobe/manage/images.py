from __future__ import division, print_function
from PIL import Image
import click
from click import echo, style

from ...application import app, db
from pathlib import Path
from ...core.models import Sample
from ..models import ProbeImage

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

def import_image(sample, image, info):
    info = {k:v for k,v in get_info(info)}
    name = sanitize_name(image.stem)
    echo(name)
    model = db.session.query(ProbeImage)\
        .filter_by(name=name).first()
    if not model:
        data = {k:float(info[v])\
            for k,v in field_map.items()}
        model = ProbeImage(
            name=name,
            sample_id=sample.id,
            **data)

    try:
        assert model.path.is_file()
    except AssertionError:
        im = Image.open(str(image))
        im.save(str(model.path))

    db.session.add(model)

@click.command()
def import_images():
    """
    Imports probe images into the database.
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
