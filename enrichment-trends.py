import numpy as N
import matplotlib.pyplot as P
import periodictable as pt
from xenoliths.application import app
from xenoliths.SIMS.query import sims_data
from xenoliths.core.models import Sample

with app.app_context():

    df = sims_data(averaged=True, dataframe=True)

    colors = {s.id: s.color
        for s in Sample.query
            .filter_by(xenolith=True)
            .order_by(Sample.id)
            .all()}

df = (df
        [df['mineral'] == 'cpx']
        .drop('mineral',axis=1)
        .drop('element',axis=1))

tab = df.pivot(
        columns='symbol',
        index='sample_id')
tab.columns = tab.columns.droplevel()
tab['color'] = tab.index.map(colors.get)

fig, ax = P.subplots(1, figsize=(5,5))

nv = lambda x: x.nominal_value

tab['HREE_proxy'] = 1/tab['Lu'].apply(nv)
tab['LREE_proxy'] = (tab['La']-tab['Lu']).apply(nv)
ax.scatter(
    tab['HREE_proxy'],
    tab['LREE_proxy'],
    c=tab['color'])

ax.set_ylabel("La - Lu (proxy for LREE enrichment)")
ax.set_xlabel(r"Lu$^{-1}$ (proxy for depletion)")

val = ('HREE','LREE')
for i,r in tab.iterrows():
    loc = tuple(r[v+'_proxy'] for v in val)
    ax.annotate(i,
        loc,xytext=(5,5), textcoords='offset points')

fig.savefig("build/enrichment.pdf", bbox_inches="tight")

