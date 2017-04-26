from os import path
import matplotlib
import yaml
from matplotlib import pyplot
import seaborn.apionly as sns
from colour import Color
from string import ascii_uppercase

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
    defaults = dict(lum=0.1, sat=0)
    defaults.update(kwargs)
    for color in colors:
        c = Color(color)
        c.luminance += defaults['lum']
        c.saturation += defaults['sat']
        yield c.hex

def axis_labels(*axes, pad=0.14, ypos=1, **kwargs):
    defaults = dict(
        color="#888888", fontsize=20,
        weight='bold', va='top')
    defaults.update(kwargs)

    for i, a in enumerate(axes):
        a.text(-pad,ypos, ascii_uppercase[i],
               transform=a.transAxes, **defaults)
