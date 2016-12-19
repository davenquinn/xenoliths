# -*- coding: utf-8 -*-
import re
import yaml
import codecs
import pypandoc
from pandas import isnull
from os import path
import numpy as N
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader
from .units import filter_SI_units

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
    (re.compile(r'\.\.\.+'), r'\\ldots')
)

def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

def nominal(value,rounding=2):
    if isnull(value):
        return '--'
    fs = "{0:."+str(rounding)+"f}"
    try:
        return fs.format(value.n)
    except AttributeError:
        return fs.format(value)

def uncertain(value,rounding=2):
    fs = "{0:."+str(rounding)+"f}"
    d = tuple(fs.format(i)\
        for i in (value.n, value.s))
    try:
        return "$\pm$".join(d)
    except AttributeError:
        return value

__dirname = path.dirname(__file__)
templates = path.join(__dirname,"templates")

dirs = ['templates',path.join(__dirname,'templates')]
tex_renderer = Environment(
    block_start_string = '<#',
    block_end_string = '#>',
    variable_start_string = '<<',
    variable_end_string = '>>',
    comment_start_string = '<=',
    comment_end_string = '=>',
    loader = FileSystemLoader(dirs))
tex_renderer.filters["escape_tex"] = escape_tex
tex_renderer.filters["un"] = uncertain
tex_renderer.filters["n"] = nominal

def make_figure(data):
    data["caption"] = pandoc_processor(data["caption"])
    fig = tex_renderer.get_template("figure.tex")
    return fig.render(**data)

def make_table(data):
    data["caption"] = pandoc_processor(data["caption"])
    p = path.join(__dirname,"..",data["location"])
    if 'notes' in data:
        data["notes"] = OrderedDict(sorted(data["notes"].items()))
    try:
        with open(p) as f:
            data["content"] = f.read()
    except:
        data["content"] = "Cannot find table"
    fig = tex_renderer.get_template("table.tex")
    return fig.render(**data)

dir = 'collected'

replacements = [
    (u"ºC","\\celsius{}"),
    ("\~",'~'),
    ("~","\~")
]

def process_text(directory):

    body_renderer = Environment(
        block_start_string = '[[*',
        block_end_string = '*]]',
        variable_start_string = '[[',
        variable_end_string = ']]',
        comment_start_string = '[[=',
        comment_end_string = '=]]',
        loader = FileSystemLoader(directory))
    body_renderer.filters["figure"] = make_figure
    body_renderer.filters["table"] = make_table

    with open(path.join(directory,"includes.yaml")) as f:
        includes = yaml.safe_load(f)
    def update(label,item):
        loc = item.pop('location',None)
        if loc:
            ex = path.splitext(loc)[1]
            loc = path.join(dir,label+ex)
        item['location'] = loc
        _ = dict(
            scale=None,
            label=label,
            type='figure',
            two_column=False,
            width='20pc',
            sideways=False,
            caption="")
        _.update(**item)
        star = "*" if _["two_column"] else ""

        if _['two_column']:
            _['width'] = '42pc'

        _["env"] = _["type"] + star
        return _
    items = {l: update(l,d)
            for l,d in includes.items()}

    tpl = body_renderer.get_template("body.md")
    text = tpl.render(**items)
    for t in replacements:
        text = text.replace(*t)

    text = filter_SI_units(text)
    return pandoc_processor(text)
