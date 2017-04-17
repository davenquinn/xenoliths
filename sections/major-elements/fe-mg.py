from __future__ import division
import numpy as N
from paper.plot_style import update_axes
from matplotlib.pyplot import subplots
from xenoliths import app
from sqlalchemy import or_
from xenoliths.models import Sample, ProbeMeasurement, ProbeDatum, Tag
from paper.query import not_bad
from sys import argv
from colour import Color

minerals = ['ol','cpx','opx']
m = ProbeMeasurement
d = ProbeDatum

def process_data(measurements):
    for m in measurements:
        ox = lambda x: m.oxide(x).molar_percent
        color = m.sample.color
        if m.sample_id == 'CK-1':
            color = '#dddddd'
        c = Color(color)
        c.luminance += 0.1
        ec = c.hex

        yield ox('MgO'),ox('FeO'),ec,color

with app.app_context():
    q = (ProbeMeasurement.query.join(Sample)
        .filter(Sample.id.notin_(['CK-D1','CK-D2']))
        .filter(m.oxide_total > 98)
        .filter(not_bad()))

    fig, ax = subplots(figsize=(4,3.5))

    def scatter_plot(query, **kwargs):
        data = list(process_data(query.all()))
        x,y,colors,edgecolors = zip(*data)
        return ax.scatter(x,y,c=colors,
            edgecolors=edgecolors, alpha=0.5, **kwargs)


    lava = scatter_plot(q.filter(Sample.id == 'CK-1'),
                        marker='s', s=8)
    xeno = scatter_plot(q.filter(Sample.id != 'CK-1'))

    legend = ax.legend([lava,xeno],
            ['Host lava: CK-1','Xenoliths: CK-2 to CK-7'],
              prop=dict(size=6),
              loc='upper left')
    fr = legend.get_frame()
    fr.set_lw(0.5)

    n = 8
    ax.set_xlim([12,65])
    ax.set_ylim([0,22.5])
    ax.autoscale(False)

    lines = N.linspace(66,90,n+1)
    for i,num in enumerate(lines):
        ax.plot([0,num],[0,100-num],
                color='#dddddd',
                linewidth=0.5,
                linestyle='dashed',
                dashes=(2,2),
                zorder=-5)

        angle = N.arctan2(
            (100-num),num)

        aspect = ax.get_data_ratio()

        real_angle = N.arctan2((100-num)/aspect,num)
        xstart = 22
        h = xstart+(50-xstart)*i/n
        x = N.cos(angle)*h
        y = N.sin(angle)*h
        ax.text(x,y,"{:.0f}".format(num),
                color='#aaaaaa', size=6,
                backgroundcolor='white',
                rotation=N.degrees(real_angle),
                horizontalalignment='center',
                verticalalignment='center',
                zorder=-4)

    ax.set_xlabel("MgO (molar %)")
    ax.set_ylabel("FeO (molar %)")

    ax.text(32,10.8,"Mg #",rotation=-20, color="#aaaaaa",size=5)
    props = dict(color='#aaaaaa', size=6,
                 horizontalalignment='center',
                 verticalalignment='center')
    ax.text(43,3.2,"Orthopyroxene",**props)
    ax.text(22,1.4,"Clinopyroxene",**props)
    ax.text(60,4.8,"Olivine",**props)
    ax.text(42,11.5,"Spinel",**props)
    ax.text(53,21,"Phenocryst olivine",**props)

    update_axes(ax)

    fig.savefig(argv[1], bbox_inches='tight')

