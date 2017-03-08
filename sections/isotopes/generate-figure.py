from __future__ import division, print_function
from pandas import DataFrame
import yaml
from sys import argv
import numpy as N
import matplotlib as M

from matplotlib import pyplot as P
from paper.plot_style import update_axes
from scipy import interpolate
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from calculations import Epsilon_Nd

from xenoliths import app, db
from xenoliths.models import Sample

data = DataFrame.from_csv("isotope-data.tsv",sep='\t')

with app.app_context():
    _ = (db.session.query(Sample)
        .filter_by(xenolith=True).all())
    colors = {s.id: s.color for s in _}
    data['color'] = data.index.map(lambda i:colors[i])
data.reset_index(level=0, inplace=True)

x = data["87Sr/86Sr(0)"]
y = data['Epsilon Nd']

fig, ax = P.subplots(figsize=(4,3))

ax.plot(x,y,'ko')

ax.set_xlabel(r'$^{87}$Sr/$^{86}$Sr')
ax.set_ylabel(r"$\epsilon_{Nd}$")
ax.set_ylim([-5,14])
ax.set_xlim([0.7015,0.7068])


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
        xy=(0.7062,-4.4),**kw)
ax.annotate("Primitive\nMantle", xy=(0.70435,1.9),**kw)

kw['ha']='left'
ax.annotate("Depleted Mantle", xy=(0.70305,9.5),**kw)

ax.text(0.7034,5.8, 'Mantle Array',
        ha = 'center',
        va = 'center',
        color = '#bbbbbb',
        fontsize = 12,
        rotation = -47)

# Plot splines
areas = {
    'continental': '#cccccc',
    'depleted-mantle': '#aaaaaa',
    'bulk-earth': '#dddddd',
    'mantle-array': '#eeeeee'
}

patches = []
for k,color in areas.items():
    with open('plot-data/'+k+'.txt') as f:
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

## Add annotation

arrow = dict(
    facecolor='black',
    arrowstyle='-|>')

ax.annotate('Crystal Knob suite',
            xy=(x.mean(), y.mean()),
            ha='center',
            va='baseline',
            xytext=(20,10),
            fontsize=9,
            textcoords='offset points')

update_axes(ax)

fig.tight_layout()
fig.subplots_adjust(left=0.06,bottom=0.06)
fig.savefig(argv[1], bbox_inches="tight")

