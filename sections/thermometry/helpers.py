from colour import Color
from paper.plot_style import lighten
from matplotlib.colors import colorConverter

def label(i):
    s = r"T$_\mathregular{"+i+r"}$"
    return s + u" (\u00b0C)"

def scatter_options(color, loc='core', **kwargs):
    base = dict(marker="o", s=20)
    base.update(**kwargs)
    #color = Color(color)
    if loc == "core":
        fc = next(lighten(color, lum=0.1))
        return dict(color=fc, edgecolor=color, alpha=0.5)
    elif loc == "rim":
        opaque = colorConverter.to_rgba(color)
        transparent = colorConverter.to_rgba(color,alpha = 0.5)
        return dict(edgecolor=transparent, color=(1,1,0,0.0), **base)
