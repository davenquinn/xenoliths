from __future__ import division
import numpy as N
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure
from matplotlib.gridspec import GridSpec
from xenoliths import app
from sqlalchemy import or_
from xenoliths.models import Sample, ProbeMeasurement, ProbeDatum, Tag
from paper.query import not_bad
from paper.plot_style import update_axes, axis_labels, lighten
from sys import argv
from colour import Color
from seaborn.apionly import despine
import matplotlib.pyplot as P
import yaml
from pandas import DataFrame
from query import spinel_data
from spinel_calc import correct_spinel, get_cations

minerals = ['ol','cpx','opx']
m = ProbeMeasurement
d = ProbeDatum

def edge_color(color):
    c = Color(color)
    c.luminance += 0.1
    return c.hex

def process_data(measurements):
    for m in measurements:
        ox = lambda x: m.oxide(x).molar_percent
        color = m.sample.color
        if m.sample_id == 'CK-1':
            color = '#dddddd'
        ec = edge_color(color)
        yield ox('MgO'),ox('FeO'),ec,color

with app.app_context():
    q = (ProbeMeasurement.query.join(Sample)
        .filter(Sample.id.notin_(['CK-D1','CK-D2']))
        .filter(m.oxide_total > 98)
        .filter(not_bad()))

    fig = figure(figsize=(4,7.5))

    gs = GridSpec(3,2, height_ratios=[2,1,1], width_ratios=[2.5,3.5], wspace=0.04)
    ax = fig.add_subplot(gs[0,:2])

    def scatter_plot(query, **kwargs):
        data = list(process_data(query.all()))
        x,y,colors,edgecolors = zip(*data)
        return ax.scatter(x,y,c=colors,
            edgecolors=edgecolors, alpha=0.5, **kwargs)


    lava = scatter_plot(q.filter(Sample.id == 'CK-1'),
                        marker='s', s=8)
    xeno_query = q.filter(Sample.id != 'CK-1')
    xeno = scatter_plot(xeno_query)

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

    aspect = ax.get_data_ratio()


    lines = N.linspace(66,90,n+1)
    xvals = N.linspace(22,50,len(lines))
    v = lines/100
    yvals = xvals*(1-v)/v

    for i,(num,*loc) in enumerate(zip(lines, xvals, yvals)):
        ax.plot([0,num],[0,100-num],
                color='#dddddd',
                linewidth=0.5,
                linestyle='dashed',
                dashes=(2,2),
                zorder=-5)

        angle = N.arctan2(
            (100-num),num)


        real_angle = N.arctan2((100-num)/aspect,num)
        xstart = 22
        h = xstart+(50-xstart)*i/n

        print(loc)
        ax.text(*loc,"{:.0f}".format(num),
                color='#aaaaaa', size=6,
                backgroundcolor='white',
                rotation=N.degrees(real_angle),
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transData,
                zorder=-4)

    ax.set_xlabel("MgO (molar %)")
    ax.set_ylabel("FeO (molar %)")

    ax.text(32,11.6,"Mg #",rotation=-20, color="#aaaaaa",size=5)
    props = dict(color='#aaaaaa', size=8,
                 horizontalalignment='center',
                 verticalalignment='center')
    ax.text(43,3.2,"Orthopyroxene",**props)
    ax.text(22,1.4,"Clinopyroxene",**props)
    ax.text(60,4.8,"Olivine",**props)
    ax.text(42,11.2,"Spinel",**props)
    ax.text(53,21,"Phenocryst olivine",**props)

    update_axes(ax)

    def process_data():
        for m in xeno_query.all():
            ox = lambda x: m.oxide(x).molar_percent
            color = m.sample.color
            ec = edge_color(color)
            yield ox('SiO2'),m.mg_number,ec,color

    data = list(process_data())
    x,y,colors,edgecolors = zip(*data)

    ax2 = fig.add_subplot(gs[1,0])
    ax2.scatter(x,y,c=colors,
        edgecolors=edgecolors, alpha=0.5)
    ax2.set_xlim(32,34.5)


    ax3 = fig.add_subplot(gs[1,1], sharey=ax2)
    ax3.scatter(x,y,c=colors,
        edgecolors=edgecolors, alpha=0.5)
    ax3.set_xlim(47.5,51)
    ax2.set_ylim(86,92)

    v = dict(va='top', fontsize=10, color='#888888')
    ax2.text(32.2,92, "Olivine", **v)
    ax3.text(49.4,92, "Pyroxene", **v)

    update_axes(ax2)
    despine(ax=ax3,left=True)
    ax2.set_ylabel("Mg#")
    ax3.yaxis.set_visible(False)

    ax4 = fig.add_subplot(gs[1,:2])
    ax4.axis('off')
    ax3.set_xlabel("SiO2 (molar %)")
    ax3.xaxis.set_label_coords(0.15,-0.18)

    ### Spinel Cr ###
    ax5 = fig.add_subplot(gs[2,:2])

    spinels = spinel_data()
    colors = [s.sample.color for s in spinels]

    edgecolors = list(lighten(*colors, lum=0.1))

    data = [correct_spinel(s, uncertainties=False) for s in spinels]

    # Use all tetrahedral cations in the calculation of corrected Cr#
    cr_number = [c['Cr']/(c['Cr']+c['Al'])*100 for c in data]
    mg_number = [c['Mg']/(c['Mg']+c['Fe'])*100 for c in data]

    ax5.scatter(cr_number,mg_number,
            c=edgecolors,
            edgecolor=colors,
            alpha=0.8,
            label='Corrected')
    ax5.set_ylim([70,85])
    ## Annotations
    # Group data
    with open("spinel-cr-annotations2.yaml",'r') as f:
        annotation_data = yaml.load(f.read())

    samples = [s.sample.id for s in spinels]
    df = DataFrame(
        data=N.array([cr_number, mg_number]).T,
        index=samples)

    vals = annotation_data['default']
    for id in df.index.unique():
        sm = df.ix[df.index == id]
        pos = tuple(sm.mean())

        v_ = annotation_data.get(id,None)
        if v_ is not None:
            v_ = dict(vals,**v_)
        ax5.annotate(id, xy=pos, **v_)

    ax5.set_ylabel('Spinel Mg# (corr.)')
    ax5.set_xlabel('Spinel Cr#')

    update_axes(ax5)


    axis_labels(ax,ax4,ax5, fontsize=14, pad=.15)
    fig.savefig(argv[1], bbox_inches='tight')

