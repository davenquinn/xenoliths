#!/usr/bin/env python

import numpy as N
from xenoliths import app
from xenoliths.thermometry import pressure, barometers
from sys import argv
from operator import attrgetter
from pickle import dump
from subprocess import call

call(["redo-ifchange",pressure.__file__,barometers.__file__])

def pressure_data():
    data = pressure.pressure_measurements(uncertainties=False, n=5, monte_carlo=200)
    for sample, res in data:
        yield dict(
            temperature=N.array([t.temperature for t in res]).flatten(),
            depth=N.array([t.depth for t in res]).flatten(),
            sample_id=sample.id,
            sample_color=sample.color)

outfile = argv[3]
with app.app_context():
    data = list(pressure_data())
with open(outfile,'w') as f:
    dump(data,f)
