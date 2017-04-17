from __future__ import print_function
import pandas as P
from io import StringIO
from IPython import embed

class MeltsDataset(object):
    """
    Object representing the contents of a MELTS file
    """
    def __init__(self, filename):
        self.title = "Untitled"
        trace, composition = '',''
        with open(filename) as f:
            for line in f:
                parts = line.split(': ')
                if len(parts) != 2:
                    continue
                t, value = parts

                if t == 'Title':
                    self.title = value.strip()
                elif t == 'Initial Temperature':
                    self.temperature = float(value.strip())
                elif t == 'Initial Pressure':
                    self.pressure = float(value.strip())
                elif t == 'Initial Trace':
                    trace += value
                elif t == 'Initial Composition':
                    composition += value

        get_df = lambda x:  P.read_table(
            StringIO(x),
            names=['Element','Value'],
            header=None,
            index_col=0,
            delim_whitespace=True)

        self.trace = get_df(trace)
        self.composition = get_df(composition)

    def __repr__(self):
        return "MeltsDataset: {}".format(self.title)

get_melts_data = lambda fn: MeltsDataset(fn)
