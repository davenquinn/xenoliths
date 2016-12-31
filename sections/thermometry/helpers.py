from chroma import Color

def label(i):
    s = r"T$_\mathregular{"+i+r"}$"
    return s + u" (\u00b0C)"

def scatter_options(color, loc='core', **kwargs):
    base = dict(marker="o", s=20)
    base.update(**kwargs)
    color = Color(color)
    if loc == "core":
        color.alpha = 0.5
        return dict(color=color.rgb)
    elif loc == "rim":
        color.alpha = 0.2
        f = Color("#ffffff")
        f.alpha = 0
        return dict(edgecolor=color.rgb, color=f.rgb, **base)
