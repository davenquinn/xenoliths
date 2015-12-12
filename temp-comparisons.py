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

from helpers import label,scatter_options

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

thermometers = {
    "ta98":{"name": "TA98"},
    "bkn":{"name": "BKN"},
    "ca_opx":{"name": "Ca-in-Opx"},
    "ca_opx_corr":{"name": "Ca-Opx"} # Nimis and Grutter, 2010 
    }

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

fig, axes = P.subplots(3,1,figsize=(4,9),sharex=True)
fig.subplots_adjust(hspace=0)

# Violin plot
def comparator(x):
	"""Sorts data in ascending order"""
	return N.array(x["core"]["ta98"]["sep"]).mean()

data.sort(key=comparator)

ax = axes[0]

for i,s in enumerate(data):
    for loc in ('core','rim'):
        x = s[loc]["ta98"]["sep"]
        popts = scatter_options(s['color'],loc)
        y = i
        if loc == 'rim':
            y -= 0.2
        else:
            y += 0.1
            popts['s'] = 60
        y = [y]*len(x)
        ax.scatter(x,y, **popts)

ax.set_ylim([-0.5,len(data)-0.5])
ax.set_ylabel("Samples")
ax.set_yticks(range(len(data)))
ax.set_yticklabels([s['id'] for s in data])

plots = ('bkn','ca_opx_corr')
for thermometer,ax in zip(plots,axes[1:]):
    ids = ('ta98',thermometer)
    names = [thermometers[th]["name"] for th in ids]

    for sample in data:
        name = sample["id"]

        for a_loc in ["core", "rim"]:
            values = [sample[a_loc][i]["sep"] for i in ids]
            popts = scatter_options(sample['color'],a_loc)
            ax.scatter(values[0], values[1], **popts)

    ax.set_ylabel(label(names[1]))
    ax.autoscale(False)
    ax.set_xlim([900,1200])
    if thermometer == 'ca_opx_corr':
        ax.set_ylim([925,1225])
    else:
        ax.set_ylim([975,1275])
    ax.plot([0,1800],[0,1800],color="#cccccc", zorder=-20)

axes[-1].set_xlabel(label(names[0]))

path = os.path.join("build", "temp-comparisons.pdf")
fig.savefig(path, bbox_inches="tight")
