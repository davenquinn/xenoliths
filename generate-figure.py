from __future__ import division, print_function
from pandas import DataFrame
from sys import argv
import numpy as N
import matplotlib as M
from matplotlib import pyplot as P
from scipy import interpolate

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
ax.annotate("Crystal Knob",
        xy=(x.mean(),y.mean()), xycoords="data", textcoords="offset points", xytext=(15,-4))

ax.axhline(y=0, color="#999999", linestyle="dotted")
ax.axvline(x=.7045, color="#999999", linestyle="dotted")

# Bulk earth from DePaolo and Wasserburg, 1976
ax.annotate("Bulk Earth", xy=(.7045,0), xycoords="data", textcoords="offset points", xytext=(5,5))

# Plot splines
areas = {
    'continental': '#cccccc',
    'depleted-mantle': '#aaaaaa',
    'bulk-earth': '#dddddd',
    'mantle-array': '#eeeeee'
}

def spline_interpolate(coords, n=100):
    nt = N.linspace(0, 1, n)
    t = N.zeros(coords.shape)
    t[1:] = N.sqrt((x[1:] - x[:-1])**2 + (y[1:] - y[:-1])**2)
    t = N.cumsum(t)
    t /= t[-1]
    x = [i[0] for i in coords]
    y = [i[1] for i in coords]
    x2 = interpolate.spline(t, x, nt)
    y2 = interpolate.spline(t, y, nt)
    return [(x,y) for x,y in zip(x2,y2)]

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

fig.savefig(argv[1], bbox_inches="tight")

