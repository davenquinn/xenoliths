import click
from geotherm.units import u

from .calc import underplating, forearc_case

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    """ Solve the basic heat flow models."""

    scenarios = [
        (80,60),(70,50),(60,40),(50,30),(40,20),(30,10),(28,2)]

    for sub_age,oc_age in scenarios:
        forearc_case("forearc-{0}-{1}".format(sub_age,oc_age),
            u(sub_age+oc_age,"Myr"), u(sub_age,"Myr"))

    underplating()

