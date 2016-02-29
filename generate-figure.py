from __future__ import division, print_function
from pandas import DataFrame
from sys import argv
import numpy as N
import matplotlib as M
from matplotlib import pyplot as P
from scipy import interpolate
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

data = DataFrame.from_csv("isotope-data.tsv",sep='\t')

x = data["87Sr/86Sr(0)"]
y = data['Epsilon Nd']

fig = P.figure()
ax = fig.add_subplot(111)
ax.plot(x,y, "ko")

ax.set_xlabel(r'$^{87}$Sr/$^{86}$Sr')
ax.set_ylabel(r"$\epsilon_{Nd}$")
ax.set_ylim([-5,12])
ax.set_xlim([0.7015,0.708])


ax.axhline(y=0, color="#999999", linestyle="dotted")
ax.axvline(x=.7045, color="#999999", linestyle="dotted")

# Bulk earth from DePaolo and Wasserburg, 1976
ax.annotate("Bulk Earth",
        xy=(.7045,0),
        xycoords="data",
        textcoords="offset points",
        xytext=(5,5),
        fontsize=9)
kw = dict(xycoords="data",
    color="#888888",
    ha='center',
    va='center')
ax.annotate("Continental",
        xy=(0.7065,-4.4),**kw)
ax.annotate("Primitive\nMantle", xy=(0.70425,1.9),**kw)

kw['ha']='left'
ax.annotate("Depleted Mantle", xy=(0.703,10.9),**kw)

ax.text(0.7031,4, 'Mantle Array',
        ha = 'center',
        va = 'center',
        color = '#bbbbbb',
        fontsize = 20,
        rotation = -51)

# Plot splines
areas = {
    'continental': '#cccccc',
    'depleted-mantle': '#aaaaaa',
    'bulk-earth': '#dddddd',
    'mantle-array': '#eeeeee'
}

patches = []
for k,color in areas.items():
    with open('fields/'+k+'.txt') as f:
        coords = [i.strip().split() for i in f.readlines()]
        coords = [(float(a),float(b)) for (a,b) in coords]
    Path = M.path.Path
    codes = ([Path.MOVETO]
             + [Path.CURVE4]*(len(coords)-1))

    path = Path(coords, codes)
    patch = M.patches.PathPatch(path,
            facecolor=color,
            edgecolor='none',
            zorder = -20 if k == 'mantle-array' else 0)
    ax.add_artist(patch)

ax.patches = patches

axins = zoomed_inset_axes(ax, 8, loc=1)
axins.plot(x,y, 'ko')
axins.set_ylim(10.2,11.2)
axins.set_xlim(0.70225,0.7025)
for a in (axins.xaxis,axins.yaxis):
    #loc = P.MaxNLocator(4)
    #a.set_major_locator(loc)
    a.set_ticks([])

mark_inset(ax, axins, loc1=2, loc2=3, fc="none", ec="0.5")

fig.savefig(argv[1], bbox_inches="tight")

