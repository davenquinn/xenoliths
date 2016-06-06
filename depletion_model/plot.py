import contextlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import FigureCanvas

@contextlib.contextmanager
def ree_plot(fn, size=(4,6)):
    """
    Context manager to create plot with appropriate
    axes for plotting REE data
    """
    fig = Figure(figsize=size)
    fig.canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.set_yscale('log')
    yield ax
    fig.savefig(fn, bbox_inches='tight')

