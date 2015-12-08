#!/usr/bin/env python

from __future__ import division, print_function
import os
import matplotlib
import matplotlib.pyplot as P
import numpy as N
from pickle import dump, load
from chroma import Color

from xenoliths import app
from xenoliths.thermometry.results import xenoliths, sample_temperatures

cache = "build/comparison-data.pickle"

def create_data():
    with app.app_context():
        data = [sample_temperatures(s, distinct=min)
           for s in xenoliths()]
    with open(cache,"w") as f:
        dump(data,f)
    return data

try:
    with open(cache) as f:
        data = load(f)
except IOError:
    data = create_data()

font = {'family' : 'Helvetica Neue',
        'weight' : 'light',
        'size'   : 10}

matplotlib.rc('font', **font)

thermometers = {
    "ta98":{"name": "TA98"},
    "bkn":{"name": r"T$_{BKN}$"},
    "ca_opx":{"name": "Ca-in-Opx"},
    "ca_opx_corr":{"name": "Ca-in-OPX (corrected)"} # Nimis and Grutter, 2010 
    }

plots = ('bkn','ca_opx_corr')

props = {
    "core": {
        "label": "Core",
        "color": "black"
    },
    "rim": {
        "label": "Rim",
        "color": "#eeeeee",
        "edgecolor": "black"
    }
}
annotate_props = dict(xytext=(5,-5), textcoords='offset points', ha='left', va='center')

fig, axes = P.subplots(2,1,figsize=(4,6),sharex=True)
fig.subplots_adjust(hspace=0.05)

th1 = 'ta98'
for th2,ax in zip(plots,axes):
    names = [thermometers[th]["name"] for th in [th1,th2]]
    ids = [th1,th2]

    for sample in data:
        name = sample["id"]

        for a_loc in ["core", "rim"]:
            values = [sample[a_loc][i]["sep"] for i in ids]
            color = Color(sample['color'])
            if a_loc == "core":
                color.alpha = 0.5
                popts = dict(color=color.rgb)
            elif a_loc == "rim":
                color.alpha = 0.2
                f = Color("#ffffff")
                f.alpha = 0
                popts = dict(edgecolor=color.rgb, color=f.rgb)
            ax.scatter(values[0], values[1], marker="o", s=20, **popts)

    ax.set_ylabel(u"{0} \u00b0C".format(names[1]))
    ax.autoscale(False)
    ax.set_xlim([900,1200])
    if th2 == 'ca_opx_corr':
        ax.set_ylim([925,1225])
    else:
        ax.set_ylim([975,1275])
    ax.plot([0,1800],[0,1800],color="#cccccc", zorder=-20)

ax.set_xlabel(u"{0} \u00b0C".format(names[0]))

path = os.path.join("build", "thermometer-comparisons.pdf")
fig.savefig(path, bbox_inches="tight")

