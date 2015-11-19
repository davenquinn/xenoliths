from matplotlib.pyplot import subplots
from xenoliths import app
from xenoliths.models import Sample
from xenoliths.thermometry.rare_earth.plot import plot_DREE

with app.app_context():
    fig, axs = subplots(2,3,
            figsize=(6.5,5),
            sharey=True)
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
