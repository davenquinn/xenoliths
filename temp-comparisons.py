#!/usr/bin/env python

from __future__ import division, print_function
import os

import matplotlib.pyplot as P
import numpy as N
from pickle import dump, load

from xenoliths import app
from xenoliths.thermometry.results import xenoliths, sample_temperatures

cache = "build/comparison-data.pickle"

def create_data():
    with app.app_context():
        data = [sample_temperatures(s, distinct=False)
           for s in xenoliths()]
    with open(cache,"w") as f:
        dump(data,f)
    return data

try:
    with open(cache) as f:
        data = load(f)
except IOError:
    data = create_data()

thermometers = [
    {"id":"ta98","name": "TA98"},
    {"id":"bkn", "name": r"T$_{BKN}$"},
    {"id": "ca_opx", "name": "Ca-in-Opx"},
    {"id": "ca_opx_corr", "name": "Ca-in-OPX (Nimis and Grutter, 2010 correction)"}
    ]

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

def plot_separated(th1,th2):
    names = [th["name"] for th in [th1,th2]]
    ids = [th["id"] for th in [th1,th2]]
    fig = P.figure()
    ax = fig.add_subplot(111)

    for sample in data:
        name = sample["id"]

        for a_loc in ["core", "rim"]:
            values = [sample[a_loc][i]["sep"] for i in ids]
            print(len(values[0]),len(values[1]))
            if a_loc == "core":
                popts = dict(color=sample['color'])
            elif a_loc == "rim":
                popts = dict(edgecolor=sample['color'], color="#ffffff")
            try:
                ax.scatter(values[0], values[1], marker="o", s=20, alpha=0.7, **popts)
            except ValueError as err:
                print(err)


    ax.set_xlim([900,1150])
    ax.set_ylim([900,1150])
    ax.set_xlabel(u"{0} \u00b0C".format(names[0]))
    ax.set_ylabel(u"{0} \u00b0C".format(names[1]))
    ax.autoscale(False)
    ax.plot([0,1800],[0,1800],color="#cccccc", zorder=-20)


    fig.suptitle("{0} vs. {1} (Separated, P = {2:.1f} GPa)".format(names[1], names[0],1.5))
    path = os.path.join("build", "{0}-{1}.separate.pdf".format(ids[1], ids[0]))
    fig.savefig(path, bbox_inches="tight")

for th1 in thermometers:
    for th2 in thermometers:
        if th1 == th2: continue
        plot_separated(th1,th2)

