#!/usr/bin/env python

from __future__ import division, print_function
from IPython import embed
from matplotlib.pyplot import subplots

from data import load_data, ree_data, sample_colors
from helpers import label,scatter_options

data = load_data()
rees = ree_data()

fig, axes = subplots(4,4, sharex=True, sharey=True)
fig.subplots_adjust(hspace=0,wspace=0)
thermometers = ['bkn','ta98','ca_opx_corr','ree']

def iteraxes():
    t = thermometers
    for i,row in enumerate(axes):
        for j,ax in enumerate(row):
            yield (t[j],t[i ]),ax

for (x,y), ax in iteraxes():
    for sample in data:
        for typ in ['core','rim']:
            a = sample[typ]
            if x == 'ree': continue
            if y == 'ree': continue
            dx = a[x]['sep']
            dy = a[y]['sep']
            opts =  scatter_options(sample['color'], typ)
            ax.scatter(dx,dy,**opts)
            ax.set_ylim([925,1200])
            ax.set_xlim([925,1200])

fig.savefig('build/comparison-full.pdf', bbox_inches='tight')
