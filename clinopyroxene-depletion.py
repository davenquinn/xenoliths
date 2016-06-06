"""
Read in results of fractional melting model and pick data
that best fits each sample.
"""
from __future__ import division, print_function

from sys import argv
from colour import Color
from depletion_model import get_tables, ree_plot

data = get_tables(argv[1])

# Plot results of fractional melting

d = data['clinopyroxene_0 trace'].ix[:,3:]

cscale = Color('blue').range_to('red',len(d))

with ree_plot(argv[2]) as ax:
    x = range(d.shape[1])
    for i,row in d.iterrows():
        ax.plot(x,row, color=cscale.next().rgb)
    ax.set_ylim(1e-2,1e1)

