import matplotlib.pyplot as P
import periodictable as pt
import numpy as N

from .models import SIMSMeasurement

elements = sorted(pt.elements, key=lambda x: x.number)

rare_earths = lambda d: pt.La.number <= d._element <= pt.Lu.number

def setup_figure(mineral):
    fig = P.figure(figsize=(10,8))
    ax = fig.add_subplot(111)

    ticks = [el.number for el in elements]
    labels = [el.symbol for el in elements]
    labels[pt.promethium.number] = "--"

    ax.set_yscale('log')

    ax.xaxis.set_ticks(ticks)
    ax.xaxis.set_ticklabels(labels)
    ax.set_xlim([pt.La.number-0.5,pt.Lu.number+0.5])

    ax.set_ylabel("REE: {0} / CI chondrite".format(mineral))

    return fig, ax


def plot_all(mineral, averaged=False):

    fig, ax = setup_figure(mineral)

    query = SIMSMeasurement.query.filter_by(mineral=mineral)
    for meas in query.all():
        data = list(filter(rare_earths, meas.data))
        color = meas.sample.color
        x = [i._element for i in data]
        y = N.array([i.norm.n for i in data])
        s = N.array([i.norm.s for i in data])
        ax.fill_between(x, y-s, y+s,
            facecolor=color,
            edgecolor="none",
            alpha=0.2)
        ax.plot(x,y, color=color)

    return fig
