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
def run_model(src,dst,clinopyroxene=False):

    with app.app_context():
        data = sample_ree(
            normalized=True,mode='whole_rock')
        colors = sample_colors()

    model = DepletionModel(src)
    depleted = model.fit_HREE(data)

    trace = model.tables['Solid Trace']

    fig, ax = subplots(1,1,
        figsize=(3.5, 3.5))

    ax.plot(trace.Temperature, trace.Pressure/1e4, 'k')

    ax.set_ylabel(r'Pressure (GPa)')
    ax.set_xlabel("Temperature (\u00b0C)")

    df = concat([depleted,colors],axis=1)
    ax.scatter(df.Temperature,df.Pressure/1e4,color="white",s=50, zorder=8)
    ax.scatter(df.Temperature,df.Pressure/1e4,color=df.color,s=20, zorder=10)
    for i,row in df.iterrows():
        y = 0
        x = 5
        if i in ['CK-3', 'CK-7']:
            x -= 28
            y -= 5
        ax.annotate(i,xy=(row.Temperature,row.Pressure/1e4),
            color=row.color,xytext=(x,y),textcoords='offset points')

    ax.set_ylim([2.5,0])
    ax.set_xlim([1250,1375])
    ax.annotate("garnet out",xy=(1345,2.05),
        xytext=(-28,2),textcoords='offset points',
        size=7,
        style='italic')
    ax.annotate("start: DMM at 4.0 GPa, 1400ºC",xy=(1360,2.5),
        xytext=(-2,2),textcoords='offset points', ha='right', va='bottom', size=7)


    fig.savefig(dst, bbox_inches='tight')

if __name__ == '__main__':
    run_model()

