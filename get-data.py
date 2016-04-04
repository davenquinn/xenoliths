import numpy as N
from xenoliths import app
from xenoliths.thermometry.pressure import pressure_measurements
import sys
from operator import attrgetter
from pickle import dump

def pressure_data():
    data = pressure_measurements(uncertainties=False,core=True, n=10)
    for sample, res in data:
        res = sorted(res,key=attrgetter('temperature'))
        yield dict(
            temperature=N.array([t.temperature for t in res]),
            depth=N.array([t.depth for t in res]),
            sample_id=sample.id,
            sample_color=sample.color)

outfile = sys.argv[1]
with app.app_context():
    data = list(pressure_data())
with open(outfile,'w') as f:
    dump(data,f)
