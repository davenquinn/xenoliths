import click
from functools import partial
import matplotlib
from geotherm.units import u
matplotlib.use("TkAgg")

from .database import refresh_tables
from .calc import (
    Underplated, SteadyState, ForearcCase,
    Farallon, FarallonReheated, FiniteSolver
)

@click.command()
@click.option('--debug', default=False, is_flag=True)
@click.option('--all', default=False, is_flag=True)
@click.option('-i','--implicit',default=False, is_flag=True)
@click.option('-dt','--time-step',default=None,type=float)
@click.option('--create', default=False, is_flag=True)
@click.option('--clean', default=False, is_flag=True)
@click.argument('scenarios', nargs=-1)
def cli(scenarios, debug=False, all=False,
    implicit=False, time_step=None,
    create=False, clean=True):
    """ Solve the basic heat flow models."""

    if create:
        refresh_tables()
        return

    registry = {
        "farallon": Farallon(),
        "steady-state": SteadyState()}

    forearc_list = [
        (80,60),(70,50),(60,40),(50,30),(40,20),(30,10),(28,2)]
    for sub_age,oc_age in forearc_list:
        case = ForearcCase(sub_age,oc_age)
        registry[case.name] = case

    for dT in (0,2,4):
        case =  FarallonReheated(dT)
        registry[case.name] = case

        case = Underplated(dT)
        registry[case.name] = case

    # Run scenarios requested
    if all:
        scenarios = registry.keys()
    if len(scenarios) == 0:
        click.echo("Specify scenario names or --all")
        click.echo("Possible scenarios:")
        for i in registry:
            click.echo("  "+i)
        return

    FiniteSolver.set_defaults(type=
        'implicit' if implicit else 'crank-nicholson')

    if time_step is not None:
        dt = u(time_step,'Myr')
        click.echo("Target dt for finite solver: {}".format(dt))
        FiniteSolver.set_defaults(time_step=dt)

    for s in scenarios:
        click.echo("Running scenario "+click.style(s,fg='green'))
        registry[s]()
        click.echo("")
