# -*- coding: utf-8 -*-
import re
from figurator import pandoc_processor
from .units import filter_SI_units
import sys

replacements = [
    (u"ºC","\\celsius{}"),
    ("\~",'~'),
    ("~","\~")
]

def process_text(stdin, stdout):
    text = stdin.read()
    for t in replacements:
        text = text.replace(*t)
    text = filter_SI_units(text)
    stdout.write(pandoc_processor(text,
            citation_backend='natbib',
            extra_args=[
                '--metadata=draft:true',
                '--filter','pandoc-comments',
                '--filter','pandoc-crossref']))
