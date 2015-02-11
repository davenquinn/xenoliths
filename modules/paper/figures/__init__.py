import click
import seaborn as sns
sns.set_context("paper")
from matplotlib import pyplot as P
from xenoliths.application import app
from xenoliths.SIMS.plot import plot_all
from xenoliths.microprobe.group import get_oxides, get_molar
from xenoliths.thermometry.results import xenoliths, core_pressures

from .pyx_ree import pyx_dree
from .trace_elements import trace_elements
from .mineral_modes import mineral_modes

@click.command()
def ree_cpx():
    """ CPX rare-earth element profile"""
    fig = plot_all("cpx")
    fig.savefig("includes/figures/generated/ree-cpx.pdf")

@click.command()
def ree_opx():
    """ OPX rare-earth element profile"""
    fig = plot_all("opx")
    fig.savefig("includes/figures/generated/ree-opx.pdf")

@click.command()
def spinel_cr():
    queryset = tagged(exclude_bad(ProbeMeasurement.query), "core")
    molar = get_molar(queryset)

@click.command()
def pressures():
    samples = xenoliths()
    temp_press = [core_pressures(s)\
        for s in samples]
    temp_press = [(t,p.n) for t,p in temp_press]
    temp, press = zip(*temp_press)
    colors = [s.color for s in samples]
    fig, ax = P.subplots()
    ax.scatter(temp, press, s=5, c=colors)
    fig.savefig("includes/figures/generated/pressures.pdf")

cmds = {
    "ree-cpx": ree_cpx,
    "ree-opx": ree_opx,
    "pressures": pressures,
    "pyx-dree": pyx_dree,
    "ree": trace_elements,
    "modes": mineral_modes
    }


