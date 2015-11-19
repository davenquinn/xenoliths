import numpy as N
import matplotlib.pyplot as P
import periodictable as pt
from xenoliths.application import app
from xenoliths.SIMS.query import sims_data
from xenoliths.core.models import Sample

with app.app_context():

    data = sims_data(averaged=True)

    colors = {s.id: s.color
        for s in Sample.query
            .filter_by(xenolith=True)
            .order_by(Sample.id)
            .all()}

E = lambda s: getattr(pt.elements, s)

fig, ax = P.subplots(1, figsize=(5,5))

minerals = ("cpx","opx")

is_ree = lambda n: pt.La.number <= n <= pt.Lu.number

elements = [el for el in pt.elements if is_ree(el.number)]

ticks = [el.number for el in elements]
symbols = [el.symbol for el in elements]

for sample_id, meas in data.items():
    color = colors[sample_id]

    for mineral in minerals:
        els, d = zip(*meas[mineral].items())
        x = N.array([E(s).number for s in els])
        valid = N.array([is_ree(i) for i in x])
        x = x[valid]
        d = N.array(d)[valid]
        u = N.array([m.n for m in d])
        s = N.array([m.s for m in d])

        # Dirty hack to prevent weird error artifacts
        s[s > u] /= 2
        # Should maybe implement proper log errors
        # (i.e. not asymmetric

        ax.fill_between(x,u-s,u+s,
            facecolor=color,
            edgecolor='none',
            alpha=0.2)
        ax.plot(x,u, color=color)

ax.set_yscale('log')

ax.xaxis.set_ticks(ticks)
ax.xaxis.set_ticklabels(symbols)
ax.set_xlim([ticks[0]-0.5,ticks[-1]+0.5])

ax.set_ylabel("REE / CI chondrite")

fig.savefig("build/trace-elements.pdf", bbox_inches="tight")


