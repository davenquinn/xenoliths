from __future__ import print_function
import click
import codecs

from .util import run
from .figures import cmds
from .text import process_text, write_file

@click.group()
def cli():
    pass

@cli.group(name="build-figures", commands=cmds)
@click.option("--all", is_flag=True, default=False)
def figures(all):
    pass

@cli.command(name="create-body")
@click.argument('infile',click.Path())
@click.argument('outfile',click.Path())
@click.option('--inline-figures', default=None, type=click.Path())
@click.option('--figure-captions', default=None, type=click.Path())
def create_body(infile, outfile, inline_figures=False, figure_captions=False):
    write_file(outfile,process_text(infile,
                    inline_figures=inline_figures,
                    figure_captions=figure_captions))

@cli.command(name='standalone-table')
@click.option('--landscape',is_flag=True, default=False)
def standalone_table(landscape=False):
    """
    Wraps a table in the appropriate document headers and footers
    to be compiled on its own, and prints the result to stdout.
    """
    stdin = click.get_text_stream('stdin')
    stdout = click.get_text_stream('stdout')

    preamble = (r"""
    \documentclass[letterpaper,10pt]{article}
    \usepackage["""+
    ('landscape,' if landscape else '')
    +r"""top=1in, bottom=1in, left=1in, right=1in]{geometry}
    \usepackage{booktabs}
    \begin{document}""")
    coda = "\end{document}"

    stdout.write(preamble)
    for line in stdin:
        stdout.write(line)
    stdout.write(coda)
