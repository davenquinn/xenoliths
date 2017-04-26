# -*- coding: utf-8 -*-
from sys import argv
from PIL import Image
import matplotlib
from paper import plot_style

#matplotlib.rcParams.update({'font.size': 8})
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.cm import get_cmap
from matplotlib_scalebar.scalebar import ScaleBar
from xenoliths import app, db
from shapely.geometry import LineString
from shapely.ops import transform
from geoalchemy2.shape import to_shape
import numpy as N
from pandas import read_table
from affine import Affine
from xenoliths.microprobe.models \
        import ProbeMeasurement, ProbeSession


img = Image.open('images/cpx-phenocryst.png')

im_data = read_table('images/cpx-phenocryst.txt',
            sep="=", index_col=0, header=None)
fig, ax = plt.subplots(1,1,figsize=(6,4.5), dpi=300)

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
    linewidths=0.5,
    edgecolors='black',
    cmap=cmap, vmin=70,vmax=90,s=20,zorder=10)
cbar = fig.colorbar(scatter, ax=ax, orientation='horizontal', label='Mg #',fraction=0.04, pad=0.02)

tick_locator = MaxNLocator(nbins=6)
cbar.locator = tick_locator
cbar.update_ticks()

ax.set_xlim(0,img.size[1])
ax.set_ylim(img.size[0],0)
ax.set_axis_off()
ax.set_frame_on(False)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

scalebar = ScaleBar(1/(scale*1000), border_pad=0.3) # 1 pixel = 0.2 meter
ax.add_artist(scalebar)

fig.savefig(argv[1], bbox_inches='tight', pad_inches=0)
