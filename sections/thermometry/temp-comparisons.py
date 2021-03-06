#!/usr/bin/env python

from __future__ import division, print_function
import os
import matplotlib
import matplotlib.pyplot as P
import numpy as N

from paper.plot_style import update_axes, axis_labels
from helpers import label,scatter_options
from data import load_data
import seaborn.apionly as sns

data = load_data()

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

fig, axes = P.subplots(3,1,figsize=(3.5,7.5),sharex=True)
fig.subplots_adjust(hspace=0.08)

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
        try:
            float(y)
        except TypeError:
            y = y.nominal_value
        y = [y]*len(x)
        v = [a.nominal_value for a in x]
        ax.scatter(v,y, **popts)

ax.set_ylim([-0.5,len(data)-0.5])
ax.set_ylabel("Samples")
ax.set_yticks(range(len(data)))
ax.yaxis.set_tick_params(labelsize=10, pad=0)
ax.tick_params(axis=u'y', which=u'both',length=0)
ax.set_yticklabels([s['id'] for s in data])
sns.despine(ax=ax,left=True)

plots = ('bkn','ca_opx_corr')
for thermometer,ax in zip(plots,axes[1:]):
    ids = ('ta98',thermometer)
    names = [thermometers[th]["name"] for th in ids]

    for sample in data:
        name = sample["id"]

        for a_loc in ["core", "rim"]:
            values = [sample[a_loc][i]["sep"] for i in ids]
            popts = scatter_options(sample['color'],a_loc)
            ax.scatter(
                [i.n for i in values[0]],
                [i.n for i in values[1]], **popts)

    ax.set_ylabel(label(names[1]))
    ax.autoscale(False)
    ax.set_xlim([900,1125])
    if thermometer == 'ca_opx_corr':
        ax.set_ylim([950,1125])
    else:
        ax.set_ylim([975,1200])
    ax.plot([0,1800],[0,1800],color="#cccccc", zorder=-20)
    update_axes(ax)

axes[-1].set_xlabel(label(names[0]))
axis_labels(*axes, fontsize=16, pad=0.2)

path = os.path.join("build", "temp-comparisons.pdf")
fig.savefig(path, bbox_inches="tight")
