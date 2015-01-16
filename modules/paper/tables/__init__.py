import click
from xenoliths.thermometry.results import xenoliths,sample_temperatures
from ..text import tex_renderer, write_file
from .minerals import mineral_compositions

cmds = {
    "minerals": mineral_compositions}

@click.group(name="build-tables", commands=cmds)
def build_tables():
    pass

@build_tables.command()
def temperatures():
    """ Table of Ca-in-pyroxene temperatures"""
    template = tex_renderer.get_template("tables/temperature.tex")

    #data = [sample_temperatures(s)\
    #       for s in xenoliths()]
    data = [{"id":s.id} for s in xenoliths()]
    text = template.render(samples=data)
    write_file("includes/tables/temperatures.tex", text)

