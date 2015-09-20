import click
from geotherm.units import u

from .calc import underplating, forearc_case, farallon_case

@click.command()
@click.option('--debug', default=False, is_flag=True)
@click.option('--all', default=False, is_flag=True)
@click.argument('scenarios', nargs=-1)
def cli(scenarios, debug=False, all=False):
    """ Solve the basic heat flow models."""
    registry = {}

    forearc_list = [
        (80,60),(70,50),(60,40),(50,30),(40,20),(30,10),(28,2)]
    for sub_age,oc_age in forearc_list:
        n = "forearc-{0}-{1}".format(sub_age,oc_age)
        registry[n] = lambda: forearc_case(n,
            u(sub_age+oc_age,"Myr"), u(sub_age,"Myr"))

    registry["underplating"] = underplating
    registry["farallon"] = farallon_case

    # Run scenarios requested
    if all:
        scenarios = registry.keys()
    if len(scenarios) == 0:
        click.echo("Specify scenario names or --all")
        click.echo("Possible scenarios:")
        for i in registry:
            click.echo("  "+i)
    for s in scenarios:
        registry[s]()

