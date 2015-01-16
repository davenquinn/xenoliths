# -*- coding: utf-8 -*-
import re
import yaml
import codecs
import pypandoc
from jinja2 import Environment, FileSystemLoader

def pandoc_processor(text):
    return pypandoc.convert(text, 'latex',
            format="md", extra_args=["--natbib"])

def write_file(fn, text):
    with codecs.open(fn,"w",encoding="utf8") as f:
        f.write(text)

LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

def nominal(value,rounding=2):
    fs = "{0:."+str(rounding)+"f}"
    return fs.format(value.n)

def uncertain(value,rounding=2):
    fs = "{0:."+str(rounding)+"f}"
    d = tuple(fs.format(i)\
        for i in (value.n, value.s))
    return "$\pm$".join(d)

tex_renderer = Environment(
    block_start_string = '((*',
    block_end_string = '*))',
    variable_start_string = '(((',
    variable_end_string = ')))',
    comment_start_string = '((=',
    comment_end_string = '=))',
    loader = FileSystemLoader("source/tpl"))
tex_renderer.filters["escape_tex"] = escape_tex
tex_renderer.filters["un"] = uncertain
tex_renderer.filters["n"] = nominal

def make_figure(data):
    data["caption"] = pandoc_processor(data["caption"])
    fig = tex_renderer.get_template("figure.tex")
    return fig.render(**data)

def make_table(data):
    data["caption"] = pandoc_processor(data["caption"])
    with open("includes/tables/"+data["location"]) as f:
        data["content"] = f.read()
    fig = tex_renderer.get_template("table.tex")
    return fig.render(**data)

body_renderer = Environment(
    block_start_string = '[[*',
    block_end_string = '*]]',
    variable_start_string = '[[',
    variable_end_string = ']]',
    comment_start_string = '[[=',
    comment_end_string = '=]]',
    loader = FileSystemLoader("source/text"))
body_renderer.filters["figure"] = make_figure
body_renderer.filters["table"] = make_table

def process_text():
    with open("source/includes.yaml") as f:
        includes = yaml.safe_load(f)
    for l,d in includes.items():
        if not "type" in d:
            d["type"] = "figure"
        if not "two_column" in d:
            d["two_column"] = False
        star = "*" if d["two_column"] else ""
        d["env"] = d["type"] + star
        if not "width" in d:
            d["width"]="20pc"
        d["label"] = l

    tpl = body_renderer.get_template("body.md")
    return pandoc_processor(tpl.render(**includes))
