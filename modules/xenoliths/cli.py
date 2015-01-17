import click

from werkzeug.contrib.profiler import ProfilerMiddleware

from .application import app, db
from .microprobe.manage import ProbeCommand
from .thermometry.manage import TemperatureCommand
from .database.manage import DBCommand
from .SIMS import SIMSCommand
from IPython import embed

commands = {
    "SIMS": SIMSCommand,
    "temperature": TemperatureCommand,
    "probe": ProbeCommand,
    "db": DBCommand}

cli = click.Group(name="Xenoliths", commands=commands)

@cli.command()
@click.option("--profile",
        is_flag=True,
        default=False,
        help="Use werkzeug profiler")
def serve(profile):
    """Run the application server"""
    if profile:
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(
            app.wsgi_app, restrictions=[30])
    app.run(debug = True, host='0.0.0.0', port=8000)

@cli.command()
def shell():
    """ Create a python interpreter inside
        the application.
    """
    from . import models as m
    click.echo("Welcome to the "\
        + click.style("Xenoliths",fg="green")\
        + " application!")
    embed()

def manager():
    with app.app_context():
        cli.main(prog_name="Xenoliths")
