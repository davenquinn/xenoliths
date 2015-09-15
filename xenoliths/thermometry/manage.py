import click

from .results import text_output
from .rare_earth import ree

TemperatureCommand = click.Group(
    help="Command to manage thermometry.")

@TemperatureCommand.command()
def results():
    echo("Temperature Results")
    text_output()

@TemperatureCommand.command()
def prepare():
    """Prepare data for calculation of T_REE"""
    keys = "SiO2 TiO2 Al2O3 Cr2O3 FeO MnO MgO CaO Na2O NiO".split()

TemperatureCommand.add_command("ree",ree)
