import click

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    """ Solves heat flow models."""
    pass

@cli.command()
def solve():
    """ Solve the basic heat flow models."""
    from .calc import solve
    solve()

@cli.command()
def plot():
    from .plot import plot
    plot()
