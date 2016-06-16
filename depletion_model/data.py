from __future__ import division, print_function

import pandas as P
import re
from sys import argv
from StringIO import StringIO
from xenoliths.SIMS.query import sims_data, element_data
from .util import element
from .melts import get_melts_data

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

def sample_ree(normalized=True):
    """
    Get REE data from database
    """
    # Whole-rock or CPX fitting
    mode = 'whole_rock'

    df = sims_data(ree_only=True, raw=True, whole_rock=True)
    df = element_data(df)
    val = df.index.get_level_values('mineral')==mode
    df = df.loc[val]
    df.index = df.index.droplevel(1)
    df.drop('n', axis=1, inplace=True)
    df.columns = [element(i) for i in df.columns]

    if normalized:
        Sun_PM = get_melts_data('literature/Sun_McDonough_PM.melts')
        PM_trace = Sun_PM.trace.ix[:,0]
        df /= PM_trace
    return df.dropna(axis=1,how='all')

