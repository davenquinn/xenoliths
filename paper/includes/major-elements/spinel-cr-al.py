#!/usr/bin/env python

import matplotlib.pyplot as P
from pandas import read_sql
from xenoliths import app,db
from xenoliths.models import ProbeDatum
from query import base_query, partial_pivot

with app.app_context():
    d = ProbeDatum

    qset = base_query(d.weight_percent)
    df = read_sql(qset.statement,db.session.bind)
    df = partial_pivot(df)

    fig, ax = P.subplots(1,figsize=(5,5))
    ax.scatter(df['Al2O3'],df['Cr2O3'], c=df['color'])
    _ = lambda x: '$\mathregular{'+x+'}$'
    ax.set_ylabel(_('Cr_2 O_3'))
    ax.set_xlabel(_('Al_2 O_3'))

    fig.savefig('build/spinel-cr.pdf')

