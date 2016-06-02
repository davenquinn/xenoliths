"""
Read in results of fractional melting model and pick data
that best fits each sample.
"""
from __future__ import division, print_function

import pandas as P
import re
from sys import argv
from StringIO import StringIO
from IPython import embed
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import FigureCanvas
from colour import Color

def prepare_dataframe(text):
    title,body = text.split('\n',1)
    title = title.strip().replace(":","")
    df = P.read_table(StringIO(body), delim_whitespace=True)
    return title, df

digit = re.compile('^\d')
def get_tables():
    """
    Process lines in results file into separate tables
    """
    with open(argv[1]) as f:
        agg = ""
        for line in f:
            if line.isspace() or line.startswith('Title:'):
                # Skip line
                continue
            if all([
                not digit.match(line),
                not line.startswith("Pressure"),
                agg]):
                # We've reached the start-over point
                yield prepare_dataframe(agg)
                agg = ""
            agg += line
        if len(agg):
            yield prepare_dataframe(agg)

data = {k:v for k,v in get_tables()}

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
