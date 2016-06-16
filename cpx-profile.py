# -*- coding: utf-8 -*-
from sys import argv
from PIL import Image
from IPython import embed
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib_scalebar.scalebar import ScaleBar
from xenoliths import app, db
from shapely.geometry import LineString
from shapely.ops import transform
from geoalchemy2.shape import to_shape
import numpy as N
from pandas import read_table
from affine import Affine
from paper import plot_style
from seaborn.apionly import despine
from xenoliths.microprobe.models \
        import ProbeMeasurement, ProbeSession

img = Image.open('images/cpx-phenocryst.png')

im_data = read_table('images/cpx-phenocryst.txt',
            sep="=", index_col=0, header=None)
fig, (ax,ax2) = plt.subplots(2,1,
                figsize=(4.25,6), dpi=300,
                gridspec_kw = dict(height_ratios=[5, 1]))

ax.imshow(img)

pos = lambda loc: float(im_data.ix['Stage '+loc])
# Find affine transform
scale = img.size[1]/(pos('Xmin')-pos('Xmax'))
a = Affine.scale(-scale,scale)
a *= Affine.translation(-pos('Xmin'),-pos('Ymax'))

with app.app_context():
    measurements = (ProbeMeasurement.query
        .join(ProbeSession)
        .filter(ProbeSession.sample_id=='CK-1')
        .filter(ProbeSession.date=='2014-05-20')
        .filter(ProbeMeasurement.line_number >= 176)
        .filter(ProbeMeasurement.line_number <= 201)
        .order_by(ProbeMeasurement.line_number)
        .all())

locations = [to_shape(m.location) for m in measurements]
line = LineString([p.coords[0] for p in locations])
distances = [line.project(p)*1000 for p in locations]

projected_line = LineString([a*p.coords[0] for p in locations])
x,y = projected_line.xy

cmap = get_cmap('hot_r')

ax.plot(x,y,color='black')
scatter = ax.scatter(x,y,
   c=[m.mg_number for m in measurements],
   cmap=cmap, vmin=70,vmax=90,s=20,zorder=10)
fig.colorbar(scatter, ax=ax)
ax.set_xlim(0,img.size[1])
ax.set_ylim(img.size[0],0)
ax.set_axis_off()
ax.set_frame_on(False)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])
#ax.set_position([0,0,1,0.8])

scalebar = ScaleBar(1/(scale*1000)) # 1 pixel = 0.2 meter
ax.add_artist(scalebar)

# ax2.plot(distances, [m.mg_number for m in measurements])
# ax2.set_ylabel('Mg #')
# ax2.set_xlabel(u"Distance along transect (μm)")
# ax2.set_xlim(-10,325)
# despine(ax=ax2)

fig.subplots_adjust(wspace=0.1)
fig.tight_layout()
fig.savefig(argv[1])
