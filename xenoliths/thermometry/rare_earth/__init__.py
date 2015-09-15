"""This section implements the REE-in-two-pyroxene thermometer of Liang, Sun, and Yao (2013).
"""
from __future__ import division, print_function

import click

from ...core.models import Sample
from .calc import ree_pyroxene, rare_earths
from .pyx import BKN

@click.command()
def ree():
    """ Calculates rare-earth element temperatures using the REE-in-two-pyroxene
        thermometer of Liang, Sun, and Yao (2013).
    """
    samples = filter(lambda x: len(x.sims_measurements) > 0, Sample.query.all())

    for sample in samples:
        print(sample.id)
        ree_pyroxene(sample)
