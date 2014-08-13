from __future__ import division

import json
import seaborn as sns
from matplotlib import pyplot as P
import numpy as N

from . import results_dir

colors = dict(
    underplating="#e75348",
    farallon="#397eb8",
    monterey="#52af4a"
)

def plot():
    with open(str(results_dir("models.json")),"r") as f:
        data = json.load(f)

    fig = P.figure(figsize=(4,8))
    ax = fig.add_subplot(111)
    ax.invert_yaxis()

    y = (N.arange(len(data["farallon"])) * 10 + 5)/1000

    for k,x in data.items():
        opts = dict(
            color=colors[k],
            linewidth=2,
            label=k.capitalize())
        ax.plot(x,y, **opts)
    ax.set_xlabel(u'Temperature (\u00b0C)')
    ax.set_ylabel(u'Depth (km)')
    ax.legend()

    fig.savefig(str(results_dir("models.pdf")), bbox_inches="tight")
