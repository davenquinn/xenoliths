from __future__ import division

import json
from matplotlib import pyplot as P
import numpy as N

from . import results_dir

colors = dict(
    underplating="#e75348",
    farallon_70="#397eb8",
    farallon_60="#7fafd7",
    farallon_80="#255277",
    farallon="#397eb8",
    monterey="#52af4a"
)

def plot():
    with open(str(results_dir("models.json")),"r") as f:
        data = json.load(f)

    fig = P.figure(figsize=(4,6))
    ax = fig.add_subplot(111)
    ax.invert_yaxis()

    for k,x in data.items():
        opts = dict(
            color=colors[k],
            linewidth=2,
            label=k.capitalize())
        y = (N.arange(len(x)) * 10 + 5)/1000
        ax.plot(x,y, **opts)
    ax.set_xlabel(u'Temperature (\u00b0C)')
    ax.set_ylabel(u'Depth (km)')
    ax.legend(loc="lower left")

    ax.set_ylim([150,0])

    fig.savefig(str(results_dir("models.pdf")), bbox_inches="tight")

