"""Section of code implementing heat-flow modeling using FiPy finite element toolkit."""

from pathlib import Path
from click import echo, style
from flask.ext.script import Manager

from ..application import app

def results_dir(file=None):
    return Path(app.config.get("DATA_DIR"))/"results"/"heat-flow"/file

from .solve import solve
from .plot import plot

HeatFlowCommand = Manager()

HeatFlowCommand.command(solve)
HeatFlowCommand.command(plot)
