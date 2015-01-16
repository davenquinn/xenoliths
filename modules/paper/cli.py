import click
import codecs

from .util import run
from .figures import cmds
from .tables import build_tables
from .text import process_text, write_file

@click.group()
def cli():
    pass

@cli.group(name="build-figures", commands=cmds)
@click.option("--all", is_flag=True, default=False)
def figures(all):
    pass

cli.add_command(build_tables)

build = "build"
tmp = lambda x: build+"/"+x

def make_text():
    pandoc = "pandoc -t latex --natbib -o"
    run(pandoc, tmp("abstract.tex"), "source/text/abstract.md")
    text = process_text()
    write_file(tmp("body.tex"),text)
    run("bibtex", tmp("main.aux"))

@cli.group()
def make():
    pass

@make.command()
def formatted():
    make_text()
    run("xelatex -output-directory",build, "source/main.tex")
    run("cp", tmp("main.pdf"), "output/paper.pdf")

@make.command()
def draft():
    make_text()
    run("xelatex -output-directory",build, "source/draft.tex")
    run("cp", tmp("draft.pdf"), "output/draft.pdf")

@make.command()
def doc():
    BIBFILE = "/Users/Daven/Resources/Papers/bibtex/library.bib"
    BIBSTYLE = "source/lib/agu.csl"
    run("pandoc -t docx",
        "--bibliography="+BIBFILE,
        "--csl="+BIBSTYLE,
        "-o output/abstract.docx",
        "source/text/abstract.md")
    run("pandoc -t docx",
        "--bibliography="+BIBFILE,
        "--csl="+BIBSTYLE,
        "-o output/body.docx",
        "source/text/body.md")

@make.command()
def text():
    process_text()

