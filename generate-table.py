from xenoliths.thermometry.results import xenoliths
from paper.text import tex_renderer, write_file

@click.group(name="build-tables")
def build_tables():
    pass

@build_tables.command()
def temperatures():
    """ Table of Ca-in-pyroxene temperatures"""
    template = tex_renderer.get_template("temperature.tex")

    #data = [sample_temperatures(s)\
    #       for s in xenoliths()]
    data = [{"id":s.id} for s in xenoliths()]
    text = template.render(samples=data)
    write_file("build/temperatures.tex", text)

