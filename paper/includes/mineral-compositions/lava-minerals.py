#!/usr/bin/env python

from sys import argv
from xenoliths import app
from xenoliths.microprobe.models import ProbeMeasurement, ProbeSession
from paper.query import xenolith_minerals
from paper.query import not_bad
from figurator import tex_renderer, write_file
from pandas import read_csv, DataFrame
from sqlalchemy import or_
from IPython import embed

data = read_csv('CK-1_data.csv').set_index('id')

# We only care about lava component of CK-1
data = data[data.type != 'xenolith']

with app.app_context():
    qset = (ProbeMeasurement.query
        .join(ProbeSession)
        .filter(ProbeMeasurement.id.in_([int(i) for i in data.index]))
        .filter(ProbeSession.sample_id=='CK-1'))

    oxide_cols = [i for i in app.config.get("OXIDES")
        if i != 'NiO']

    def setup_data():
        for meas in qset.all():
            oxides = {o._oxide: o.weight_percent
                for o in meas.data}
            for k in ['oxide_total','id','mg_number','cr_number']:
                oxides[k] = getattr(meas,k)
            yield oxides

    oxides = DataFrame.from_dict(setup_data()).set_index('id')

data = data.join(oxides)
samples = [row for i,row in data.iterrows()]
text = (tex_renderer
    .get_template("lava_minerals.tex")
    .render(
        ncols=len(oxide_cols)+4,
        oxides=oxide_cols,
        samples=samples))
write_file(argv[1], text)

