from __future__ import division, print_function
from pandas import DataFrame
import yaml
from sys import argv
import numpy as N
import matplotlib as M

from matplotlib import pyplot as P
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

with open('plot-data/annotations.yaml') as f:
    aprops = yaml.load(f.read())

x = data["87Sr/86Sr(0)"]
y = data['Epsilon Nd']

fig = P.figure()
ax = fig.add_subplot(111)

ax.plot(x,y,'ko')

ax.set_xlabel(r'$^{87}$Sr/$^{86}$Sr')
ax.set_ylabel(r"$\epsilon_{Nd}$")
ax.set_ylim([-5,12])
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
ax.annotate("Primitive\nMantle", xy=(0.7043,1.9),**kw)

kw['ha']='left'
ax.annotate("Depleted Mantle", xy=(0.703,10.9),**kw)

ax.text(0.7034,5, 'Mantle Array',
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

axins = zoomed_inset_axes(ax, 8, loc=1)

for i,row in data.iterrows():
    x_ = row["87Sr/86Sr(0)"]
    xs_ = x_*(row['std err%.1']/100)
    y_ = row['Epsilon Nd']

    for lvl in (2,1):
        End = Epsilon_Nd(row)
        e = M.patches.Ellipse(
            xy=(x_,End.n),
            width=lvl*xs_,
            height=lvl*End.s,
            alpha=0.4,
            facecolor=row['color'],
            edgecolor='none')

        axins.add_artist(e)
        e.set_clip_box(axins.bbox)

    id = row["Sample Name"]
    _ = aprops.get(id,None)
    vals = aprops['default']
    if _ is not None:
        vals = dict(vals, **_)
        vals['color'] = row['color']
    axins.annotate(id, xy=(x_,y_), **vals)

axins.set_ylim(10.05,11.35)
axins.set_xlim(0.70228,0.70245)

xt = [.7023,.7024]
yt = [10.25,10.75,11.25]

axins.xaxis.get_major_formatter().set_useOffset(False)
axins.xaxis.set_ticks(xt)
axins.yaxis.set_ticks(yt)
axins.tick_params(axis='both', which='major', labelsize=9)

mark_inset(ax, axins, loc1=2, loc2=3, fc="none", ec="0.5")

fig.savefig(argv[1], bbox_inches="tight")

