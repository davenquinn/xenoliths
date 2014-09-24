from click import echo, style
from flask.ext.script import Manager

from .results import text_output
from .rare_earth import ree

TemperatureCommand = Manager(usage="Command to manage thermometry.")

@TemperatureCommand.command
def results():
    echo("Temperature Results")
    text_output()

@TemperatureCommand.command
def prepare():
    """Prepare data for calculation of T_REE"""
    keys = "SiO2 TiO2 Al2O3 Cr2O3 FeO MnO MgO CaO Na2O NiO".split()




TemperatureCommand.command(ree)
