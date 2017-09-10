from __future__ import division, print_function

import matplotlib
matplotlib.use('Agg')
from sys import argv
import numpy as N
import click
from xenoliths import app
from matplotlib.pyplot import subplots
from pandas import DataFrame, read_table, concat
from depletion_model import get_melts_data, ree_plot, sample_ree
from depletion_model.util import element, ree_only
from depletion_model import DepletionModel
from xenoliths.core import sample_colors
from ree_trends import ree_scatter
from paper.plot_style import update_axes, axis_labels

@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path())
@click.option("--clinopyroxene",is_flag=True,default=False)
def run_model(src,dst,clinopyroxene=False):

    with app.app_context():
        data = sample_ree(
            normalized=True,
            mode='cpx' if clinopyroxene else 'whole_rock')
        colors = sample_colors()

    model = DepletionModel(src)

    if clinopyroxene:
        depleted = model.fit_HREE(data, table='clinopyroxene_0 trace')
    else:
        depleted = model.fit_HREE(data)

    enrichment, multiplier = model.enrichment(data,depleted)

    # Create primitive-mantle normalized dataset
    Sun_PM = get_melts_data('literature/Sun_McDonough_PM.melts')
    PM_trace = Sun_PM.trace.ix[:,0]

    # Add NMORB
    NMORB = get_melts_data('literature/NMORB_trace.melts')
    NMORB_trace = ree_only(NMORB.trace.transpose()/PM_trace)

    # Alkali basalt
    alkali = read_table('literature/Farmer_1995-Alkali-basalt.txt',
                        comment="#", index_col=0)
    alkali /= PM_trace
    alkali_trace = ree_only(alkali)

    vals = [element(i) for i in data.columns]
    d = ree_only(depleted)

    grid=dict(height_ratios=(4.5,1), hspace=0.1, right=0.99, left=0.16)
    fig, (ax1, ax2) = subplots(2,1,
        figsize=(3.5, 6),
        gridspec_kw=grid)

    def create_main_axis(ax):
        for i,row in d.iterrows():
            c = colors.ix[row.name][0]

            # Plot real data
            series = data.ix[row.name]
            u = series.map(lambda x: x.n)
            s = series.map(lambda x: x.s)
            ax.fill_between(vals,u-s,u+s,
                facecolor=c,
                edgecolor='none',
                alpha=0.2)

            def plot(name,x,y,**kwargs):
                if i == 'CK-2':
                    kwargs['label'] = name
                else:
                    kwargs['label'] = ""
                p = ax.plot(x,y,color=c,**kwargs)

            if clinopyroxene:
                s = 'clinopyroxene'
            else:
                s = 'whole-rock'
            plot('Measured '+s,vals,u)

            # Plot calculated best fit
            plot("Modeled depleted", d.columns,row, linestyle='--', linewidth=1)

            v = enrichment.ix[row.name]
            #if i == 'CK-2':
            #    continue
            plot("Enriching melt",d.columns,v, linestyle=':', linewidth=1)

        # Plot NMORB
        ax.fill_between(NMORB_trace.columns, NMORB_trace.ix[0,:],
                NMORB_trace.ix[0,:]-0.5,
                color='#bbbbbb', linewidth=1.5, zorder=-5, label="")

        ax.fill_between(
            alkali_trace.columns,
            alkali_trace.min(),
            alkali_trace.max(),
            facecolor='#dddddd',
            edgecolor='none',
            zorder=-10,
            label="")

        ax.set_ylim(.01,100)
        ax.set_xlim(element('La')-0.1,element('Lu'))
        ax.yaxis.set_ticklabels(["{:g}".format(v) for v in ax.yaxis.get_ticklocs()])
        ax.set_ylabel("Rare-earth element abundance / Primitive Mantle")
        ax.xaxis.set_ticks(vals)
        ax.xaxis.set_ticklabels(data.columns)
        ax.set_yscale('log')
        ax.text(element('Ce')-0.5,40,"Alkali basalt",
            rotation=-28,color='#888888')
        ax.text(element('La'),5,"NMORB",
            rotation=15,color='#888888')
        legend = ax.legend(loc="upper right")
        fr = legend.get_frame()
        fr.set_lw(0.5)


    create_main_axis(ax1)
    update_axes(ax1)

    fig.subplots_adjust(top=0.99, right=0.99)
    ree_scatter(ax2, model, data, colors)
    ax2.set_ylim([0,1.2])
    ax2.set_xlabel(r'HREE depletion degrees (%)')
    ax2.set_ylabel("Enriching fluid\nassimilated (%)")
    ax2.yaxis.set_label_coords(-0.1,0.22)
    update_axes(ax2)
    axis_labels(ax1,ax2, pad=.16, fontsize=14)

    fig.savefig(dst, bbox_inches='tight')

if __name__ == '__main__':
    run_model()
