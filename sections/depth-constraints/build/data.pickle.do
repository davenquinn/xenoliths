#!/usr/bin/env python

import numpy as N
from xenoliths import app
from xenoliths.thermometry.pressure import pressure_measurements
from sys import argv
from operator import attrgetter
from pickle import dump

def pressure_data():
    data = pressure_measurements(uncertainties=False, n=4, monte_carlo=200)
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
