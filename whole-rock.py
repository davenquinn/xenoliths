#!/usr/bin/env python

from __future__ import division

from paper.query import xenolith_minerals
from xenoliths.application import app, db
from xenoliths.SIMS.quality import get_data
from xenoliths.models import Sample

with app.app_context():

    xenoliths = (db.session.query(Sample)
        .filter_by(xenolith=True))

    trace_elements = get_data()
    mineral_modes = xenolith_minerals("molar")

def cpx_ol_partitioning():
    """
    Contains the partition coefficient between
    olivine and cpx.
    Values should be taken from Witt-Eickschen and O'Neill, 2005 pp85
    """
    pass
