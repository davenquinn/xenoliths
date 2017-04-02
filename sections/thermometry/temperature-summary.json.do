#!/usr/bin/env python
# Create summary data for temperatures
# to be used in figure
from data import summary_data
from json import dumps,JSONEncoder
from sys import stdout
from subprocess import run
from dofile import redo_ifchange

redo_ifchange('build/data.pickle', ignore=['xenoliths'])

class Encoder(JSONEncoder):
    """
    Custom encoder for json
    """
    def default(self,obj):
        if obj.__class__.__name__ == 'Variable':
            return {'n':obj.n,'s':obj.s}
        else:
            return obj.__dict__

_ = dumps(summary_data(), cls=Encoder)
stdout.write(_)
