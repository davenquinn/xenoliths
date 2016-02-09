# -*- coding:utf-8 -*-

from matplotlib.pyplot import subplots
from xenoliths import app
from xenoliths.models import Sample
from xenoliths.thermometry.rare_earth import (
    ree_pyroxene, regress, temperature)

def plot_DREE(ax, sample, annotate=True):
    X,Y = ree_pyroxene(sample, 1.5) # Pressure in GPa
    res = regress(X,Y)
    T = temperature(res)

    title = u"{id}: {n:.0f}±{s:.0f} °C"\
        .format(
            id=sample.id,
            n=T.n,
            s=T.s)
    ax.plot(X,Y, "o")
    ax.plot(res.X,res.fittedvalues,"-")

    res = regress(X,Y,hree_only=True)
    ax.plot(res.X,res.fittedvalues,"-",color="#aaaaaa")

    if not annotate:
        return ax
    for x,y,t in zip(X,Y,rare_earths):
        ax.annotate(t, (x,y),
                xytext=(5,5),
                textcoords="offset points")

with app.app_context():
    fig, axs = subplots(2,3,
            figsize=(6.5,5),
            sharey=True, sharex=True)
    samples = (Sample.query
        .filter_by(xenolith=True)
        .order_by(Sample.id)
        .all())

    for ax, sample in zip(axs.flatten(), samples):
        ax = plot_DREE(ax, sample, annotate=False)
        ax.set_ylabel(r"B")
        ax.set_xlabel(r"$D_{ree}$")

    fig.subplots_adjust(hspace=0.1,wspace=0.05)
    fig.savefig("build/pyx-dree.pdf",bbox_inches="tight")
