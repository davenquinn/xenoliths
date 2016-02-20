import click
from functools import partial

from geotherm.units import u

from .database import refresh_tables
from .calc import (
    underplating, forearc_case,
    farallon_case, farallon_reheated,
    steady_state, FiniteSolver
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
        "underplating": underplating,
        "farallon": farallon_case,
        "farallon-reheated": farallon_reheated,
        "steady-state": steady_state}

    forearc_list = [
        (80,60),(70,50),(60,40),(50,30),(40,20),(30,10),(28,2)]
    for sub_age,oc_age in forearc_list:
        n = "forearc-{0}-{1}".format(sub_age,oc_age)
        args = (n,u(sub_age+oc_age,"Myr"), u(sub_age,"Myr"))
        registry[n] = partial(forearc_case,*args)

    # Run scenarios requested
    if all:
        scenarios = registry.keys()
    if len(scenarios) == 0:
        click.echo("Specify scenario names or --all")
        click.echo("Possible scenarios:")
        for i in registry:
            click.echo("  "+i)

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
