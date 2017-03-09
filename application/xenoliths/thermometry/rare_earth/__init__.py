"""
This section implements the REE-in-two-pyroxene thermometer
of Liang, Sun, and Yao (2013).
"""


import click

from ...core.models import Sample
from .calc import ree_pyroxene, rare_earths
from .plot import regress, temperature
from .pyx import BKN

@click.command()
def ree():
    """ Calculates rare-earth element temperatures using the REE-in-two-pyroxene
        thermometer of Liang, Sun, and Yao (2013).
    """
    samples = [x for x in Sample.query.all() if len(x.sims_measurements) > 0]

    for sample in samples:
        print(sample.id)
        ree_pyroxene(sample)
