from __future__ import division, print_function

from sys import argv
from depletion_model import depletion_degrees
from figurator import tex_renderer, write_file
from json import dump

sample_data = depletion_degrees()

# class Encoder(JSONEncoder):
    # """
    # Custom encoder for json
    # """
    # def default(self,obj):
        # if obj.__class__.__name__ == 'Variable':
            # return {'n':obj.n,'s':obj.s}
        # else:
            # return obj.__dict__

with open(argv[2], 'w') as f:
    dump(sample_data, f)

