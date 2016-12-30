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
from figurator import process_includes, load_spec

def pandoc_processor(text):
    return pypandoc.convert(text, 'latex',
            format="md", extra_args=["--natbib"])

def write_file(fn, text):
    with codecs.open(fn,"w",encoding="utf8") as f:
        f.write(text)

replacements = [
    (u"ºC","\\celsius{}"),
    ("\~",'~'),
    ("~","\~")
]

def process_text(directory, inline_figures=True):

    specfile = path.join(directory,"includes.yaml")
    captions = path.join(directory,"figure-captions.md")
    spec = load_spec(specfile, captions=captions)
    includes = process_includes(
            spec,
            collect_dir='collected')

    body_renderer = Environment(
        block_start_string = '[[*',
        block_end_string = '*]]',
        variable_start_string = '[[',
        variable_end_string = ']]',
        comment_start_string = '[[=',
        comment_end_string = '=]]',
        loader = FileSystemLoader(directory))
    if inline_figures:
        fn = lambda x: x
    else:
        fn = lambda x: ""
    body_renderer.filters["figure"] = fn
    body_renderer.filters["table"] = fn

    items = {l:d for l,d in includes}

    tpl = body_renderer.get_template("body.md")
    text = tpl.render(**items)
    for t in replacements:
        text = text.replace(*t)

    text = filter_SI_units(text)
    return pandoc_processor(text)
