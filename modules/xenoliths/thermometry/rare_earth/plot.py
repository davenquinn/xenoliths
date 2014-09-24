import seaborn as sns
import matplotlib.pyplot as P
from pandas import DataFrame
import periodictable as pt
import numpy as N
from .calc import ree_pyroxene, rare_earths

elements = sorted(pt.elements, key=lambda x: x.number)


def setup_figure():
    fig = P.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    ax.set_ylabel("B")
    ax.set_xlabel(r"$ln(D)-A$")
    return fig, ax

def plot_DREE(sample):
    fig, ax = setup_figure()
    X,Y = ree_pyroxene(sample, 1.5)
    df = [("el",rare_earths),("lnD_A",X),("B",Y)]
    frame = DataFrame.from_items(df)

    a = sns.lmplot("lnD_A", "B", frame, robust=True, n_boot=50, ax=ax)
    for x,y,t in zip(X,Y,rare_earths):
        ax.annotate(t, (x,y), xytext=(5,5), textcoords="offset points")
    return fig
