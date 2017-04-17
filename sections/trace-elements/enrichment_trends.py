import numpy as N
import periodictable as pt
from paper import plot_style
from paper.plot_style import lighten

def enrichment_trends(ax, df, colors):
    df = df.reset_index()
    df = (df.drop('element',axis=1))

    tab = df.pivot_table(
            columns=['symbol','mineral'],
            index='sample_id',
            values='average',
            aggfunc=lambda x: x.iloc[0])
    tab = tab.join(colors)

    nv = lambda x: x.nominal_value

    min='cpx'
    lu_idx = ('Lu', min)
    tab['HREE_proxy'] = 1/tab[lu_idx].apply(nv)
    tab['LREE_proxy'] = (tab[('La',min)]/tab[lu_idx]).apply(nv)
    colors = list(tab['color'])
    ax.scatter(
        tab['HREE_proxy'],
        tab['LREE_proxy'],
        c=list(lighten(*colors)),
        edgecolor=colors,
        alpha=0.8)

    ax.set_ylabel("La / Lu (proxy for LREE enrichment)")
    ax.set_xlabel(r"Lu$^{-1}$ (proxy for depletion)")

    mean_x = tab['HREE_proxy'].mean()

    val = ('HREE','LREE')
    for i,r in tab.iterrows():
        loc = tuple(r[v+'_proxy'] for v in val)
        v = loc[0] > mean_x
        xlabel = -5 if v else 5
        ax.annotate(i,
            loc,xytext=(xlabel,0),
                textcoords='offset points',
                va='center',
                ha='right' if v else 'left')

