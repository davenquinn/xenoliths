from __future__ import division, print_function

from sys import argv
import numpy as N
import click
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

    model = DepletionModel(argv[1])
    depleted = model.fit_HREE(data)
    enrichment, multiplier = model.enrichment(data,depleted)

    s = 100-depleted.mass
    s.name = 'Depletion'
    v = 1/multiplier
    v.name = 'Enrichment'
    df = concat([s,v,colors],axis=1)
    fig, ax = plt.subplots(figsize=(4,3.5))
    ax.scatter(df.Depletion,df.Enrichment,color=df.color,s=20)
    for i,row in df.iterrows():
        y = 0
        if i in ['CK-3','CK-6']:
            y -= 6
        ax.annotate(i,xy=(row.Depletion,row.Enrichment),
            color=row.color,xytext=(5,y),textcoords='offset points')
    ax.set_xlabel(r'HREE depletion degrees (%)')
    ax.set_ylabel(r'Mass ratio: re-enriching fluid/sample')

    ax.set_xlim([0,20])
    ax.set_ylim([0,0.012])
    fig.savefig('output/ree-trends.pdf',bbox_inches='tight')

if __name__ == '__main__':
    run_model()

