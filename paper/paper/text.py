# -*- coding: utf-8 -*-
import re
import yaml
import codecs
import pypandoc
from pandas import isnull
from os import path
import numpy as N
from collections import OrderedDict
from .units import filter_SI_units
from figurator import process_includes, load_spec
import re

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

pattern = re.compile("<!--\[\[(.+)\]\]-->")

def inline_includes(text, spec):
    includes = process_includes(
            spec,
            collect_dir='collected')
    items = {l:d for l,d in includes}
    def fn(matchobj):
        try:
            return items[matchobj.group(1)]
        except KeyError:
            # Don't replace if we can't find include
            return matchobj.group(0)
    return pattern.sub(fn,text)

def process_text(filename,**kwargs):

    specfile=kwargs.pop('inline_figures',None)
    captions=kwargs.pop('figure_captions',None)

    with codecs.open(filename,'r', encoding='utf-8') as f:
        text = f.read()

    if specfile is not None:
        spec = load_spec(specfile, captions=captions)
        text = inline_includes(text, spec)

    for t in replacements:
        text = text.replace(*t)

    text = filter_SI_units(text)
    return pandoc_processor(text)
