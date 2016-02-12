#!/usr/bin/env python

from __future__ import division

import pandas as P
from os import path, environ
from subprocess import Popen, PIPE
from xenoliths import app
from xenoliths.models import Sample

here = path.dirname(__file__)

# Get literature modal mineralogy data
data_dir = environ.get('DATA_DIR')
fn = path.join(data_dir,'literature','Mineral Modes.xlsx')
df = P.read_excel(fn, index_col=0)
df['al'] = None

# Sort data so Luffi is at end
df['order'] = df['source'].apply(lambda x: x == 'Luffi')
df = (df
    .sort('order')
    .drop('order', axis=1))

with app.app_context():
    samples = (Sample.query
        .filter_by(xenolith=True)
        .all())
    data = [s.modes() for s in samples]
    idx = [s.id for s in samples]
# Convert our data to dataframe
d = P.DataFrame(data, idx)
d = d.multiply(100)
d['color'] = [s.color for s in samples]
d['source'] = 'Quinn'
d['type'] = 'point-counting'

df = P.concat([df,d])
df['id'] = df.index
data = df.to_json(None,'records')
script = path.join(here,"generate.coffee")
p = Popen(['coffee', script],stdin=PIPE)
p.communicate(input=data)
