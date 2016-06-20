from __future__ import division, print_function

from sys import argv
import numpy as N
from xenoliths import app
from pandas import DataFrame, read_table, concat
from depletion_model import get_melts_data, ree_plot, sample_ree
from depletion_model.util import element, ree_only
from depletion_model import DepletionModel
from xenoliths.core import sample_colors
from paper import plot_style
from matplotlib import pyplot as plt

def run_model():

    with app.app_context():
        data = sample_ree(normalized=True)
        colors = sample_colors()

    # Create primitive-mantle normalized dataset
    Sun_PM = get_melts_data('literature/Sun_McDonough_PM.melts')
    PM_trace = Sun_PM.trace.ix[:,0]

    model = DepletionModel(argv[1])
    depleted = model.fit_HREE(data)
    enrichment, multiplier = model.enrichment(data,depleted)

    # Add NMORB
    NMORB = get_melts_data('literature/NMORB_trace.melts')
    NMORB_trace = ree_only(NMORB.trace.transpose()/PM_trace)

    # Alkali basalt
    alkali = read_table('literature/Farmer_1995-Alkali-basalt.txt',
                        comment="#", index_col=0)
    alkali /= PM_trace
    alkali_trace = ree_only(alkali)

    vals = map(element,data.columns)
    d = ree_only(depleted)
    with ree_plot(argv[2]) as ax:
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
                p = ax.plot(x,y,color=c,**kwargs)

            plot('Measured whole-rock',vals,u)

            # Plot calculated best fit
            plot("Modeled depleted", d.columns,row, linestyle='--')

            v = enrichment.ix[row.name]
            plot("Enriching fluid",d.columns,v, linestyle=':')

        # Plot NMORB
        ax.plot(NMORB_trace.columns, NMORB_trace.ix[0,:],
                color='#888888', linewidth=1.5, zorder=-5)

        ax.fill_between(
            alkali_trace.columns,
            alkali_trace.min(),
            alkali_trace.max(),
            facecolor='#dddddd',
            edgecolor='none',
            zorder=-10)

        ax.set_ylim(.01,100)
        ax.set_xlim(element('La')-0.3,element('Lu')+0.3)
        ax.yaxis.set_ticklabels(["{:g}".format(v) for v in ax.yaxis.get_ticklocs()])
        ax.set_ylabel("REE / Primitive Mantle")
        ax.xaxis.set_ticks(vals)
        ax.xaxis.set_ticklabels(data.columns)

        ax.text(element('Nd'),21,"Alkali basalt",
            rotation=-25,color='#888888')
        ax.text(element('La'),5,"NMORB",
            rotation=15,color='#888888')
        legend = ax.legend(loc="upper right")
        fr = legend.get_frame()
        fr.set_lw(0.5)

    s = 100-depleted.mass
    s.name = 'Depletion'
    multiplier.name = 'Enrichment'
    df = concat([s,multiplier,colors],axis=1)
    fig, ax = plt.subplots(figsize=(4.25,3.75))
    ax.scatter(df.Depletion,df.Enrichment,color=df.color,s=20)
    for i,row in df.iterrows():
        y = 0
        if i in ['CK-4','CK-6']:
            y -= 6
        ax.annotate(i,xy=(row.Depletion,row.Enrichment),
            color=row.color,xytext=(5,y),textcoords='offset points')
    ax.set_xlabel(r'HREE depletion degrees (%)')
    ax.set_ylabel(r'Mass ratio: re-enriching fluid/sample')

    fig.savefig('output/ree-trends.pdf',bbox_inches='tight')

if __name__ == '__main__':
    run_model()
