"""
Read in results of fractional melting model and pick data
that best fits each sample.
"""
from __future__ import division, print_function

import pandas as P
import re
from StringIO import StringIO
from IPython import embed

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
    with open('output/fractional-melting.tbl') as f:
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

data = {k:v for k,v in get_tables()}

print(data.keys())

embed()
