from __future__ import division

import click
from matplotlib.pyplot import subplots
import periodictable as pt
import numpy as N

from xenoliths.models import SIMSMeasurement, Sample

rare_earths = lambda d: pt.La.number <= d._element <= pt.Lu.number

@click.command()
def trace_elements():

    elements = sorted(pt.elements, key=lambda x: x.number)
    ticks = [el.number for el in elements]
    labels = [el.symbol for el in elements]
    labels[pt.promethium.number] = "--"

    samples = Sample.query\
        .filter_by(xenolith=True)\
        .order_by(Sample.id).all()

    fig, axes = subplots(2,6, figsize=(6.5,2.5),
            sharex='col',sharey='row')
    fig.subplots_adjust(hspace=0.05,wspace=0.05)
    for s_,sample in enumerate(samples):
        for r, mineral in enumerate(["cpx","opx"]):
            ax = axes[r,s_]
            measurements = SIMSMeasurement.query\
                .filter_by(sample_id=sample.id)\
                .filter_by(mineral=mineral)\
                .all()

            for meas in measurements:
                data = list(filter(rare_earths, meas.data))
                x = [i._element for i in data]
                y = N.array([i.norm.n for i in data])
                s = N.array([i.norm.s for i in data])

                ax.fill_between(x,
                    y-s, y+s,
                    facecolor="#666666",
                    edgecolor="none",
                    alpha=0.5)
                ax.plot(x,y, color="k")
            ax.set_yscale('log')

            if r==1:
                ax.xaxis.set_ticklabels(labels)

            ax.xaxis.set_ticks(ticks)
            ax.set_xlim([pt.La.number-0.5,pt.Lu.number+0.5])

        filename = "includes/figures/generated/ree.pdf"
        fig.savefig(filename, bbox_inches="tight")

