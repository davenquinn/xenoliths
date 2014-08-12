from click import echo, style
from flask.ext.script import Manager

from .results import text_output

TemperatureCommand = Manager()

@TemperatureCommand.command
def results():
    echo("Temperature Results")
    text_output()
