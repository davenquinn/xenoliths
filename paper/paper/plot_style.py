from os import path
import matplotlib
import yaml
from matplotlib import pyplot

pyplot.rcdefaults()

fn = path.join(path.dirname(__file__),'rc-settings.yaml')

with open(fn) as f:
    style_object = yaml.load(f)
for k,v in style_object.items():
    matplotlib.rc(k,**v)
