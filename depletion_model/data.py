from __future__ import division, print_function

import pandas as P
import re
from sys import argv
from StringIO import StringIO

def prepare_dataframe(text):
    title,body = text.split('\n',1)
    title = title.strip().replace(":","")
    df = P.read_table(StringIO(body), delim_whitespace=True)
    return title, df

digit = re.compile('^\d')
def __get_tables(filename):
    """
    Process lines in results file into separate tables
    """
    with open(filename) as f:
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

def get_tables(fn):
    return {k:v for k,v in __get_tables(fn)}
