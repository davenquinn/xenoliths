from .pressure import pressure_measurements
from functools import partial

colors = {
    "CK-1": "#000000",
    "CK-2": "#456AA0",
    "CK-3": "#FF9700",
    "CK-4": "#FFD100",
    "CK-5": "#3A9B88",
    "CK-6": "#FF2C00",
    "CK-7": "#8BD750"
}

def pressure_temperature(ax):
    popts = dict(marker="o", s=35, alpha=0.1)
    for r in pressure_measurements():
        vals = r.temperature,r.depth.n
        print(vals)
        ax.scatter(*vals, color=colors[r.sample.id],**popts)
    return ax
