import click
import json
from os import path
from subprocess import Popen, PIPE, STDOUT
from cairosvg import svg2pdf

from xenoliths.models import Sample

here = path.dirname(__file__)

@click.command()
def mineral_modes():
    """ Create a ternary diagram showing the modal mineralogy
        of xenolith samples.
    """
    samples = Sample.query\
        .filter_by(xenolith=True).all()
    mode_data = [dict(
        id=s.id,
        color=s.color,
        modes=s.modes())\
        for s in samples]

    data = json.dumps(mode_data)

    script = path.join(here,"scripts","modes.coffee")

    p = Popen(['coffee', script],
            stdout=PIPE,
            stdin=PIPE,
            stderr=STDOUT)
    stdout = p.communicate(input=data)[0]
    res = stdout.decode()
    click.echo(res)
    fn = "includes/figures/generated/mineral-modes.pdf"
    svg2pdf(res,write_to=fn)
