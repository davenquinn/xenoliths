#!/usr/bin/env python

from os import path
from paper.cli import cli
from paper.util import cd
from xenoliths.application import app

here = path.dirname(path.abspath(__file__))

with app.app_context():
    with cd(here):
        cli()
