from os import path
import matplotlib
import yaml
from matplotlib import pyplot
import seaborn.apionly as sns
from colour import Color

pyplot.rcdefaults()

fn = path.join(path.dirname(__file__),'rc-settings.yaml')

with open(fn) as f:
    style_object = yaml.load(f)
for k,v in style_object.items():
    matplotlib.rc(k,**v)

def update_axes(ax, ticks_out=True):
    sns.despine(ax=ax)
    if not ticks_out:
        return
    for d in [ax.get_xaxis(),ax.get_yaxis()]:
        d.set_tick_params(which='both', direction='out')

def lighten(*colors, **kwargs):
    kwargs.update(dict(lum=0.1, sat=0))
    for color in colors:
        c = Color(color)
        c.luminance += kwargs['lum']
        c.saturation += kwargs['sat']
        yield c.hex

