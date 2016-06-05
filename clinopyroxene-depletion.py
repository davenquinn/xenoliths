"""
Read in results of fractional melting model and pick data
that best fits each sample.
"""
from __future__ import division, print_function

from sys import argv
from IPython import embed
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import FigureCanvas
from colour import Color
from depletion_model import get_tables

data = get_tables(argv[1])

# Plot results of fractional melting

fig = Figure(figsize=(4,6))
fig.canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)
ax.set_yscale('log')

#d = data['Solid Trace'].ix[:,3:]
d = data['clinopyroxene_0 trace'].ix[:,3:]

cscale = Color('blue').range_to('red',len(d))

x = range(d.shape[1])
for i,row in d.iterrows():
    ax.plot(x,row, color=cscale.next().rgb)

ax.set_ylim(1e-2,1e1)
fig.savefig(argv[2], bbox_inches='tight')

embed()
