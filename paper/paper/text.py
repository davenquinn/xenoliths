# -*- coding: utf-8 -*-
import re
from .units import filter_SI_units
import sys

replacements = [
    (u"ºC",r"{$^{\circ}$C}"),
    ("\~",'~'),
    ("~","\~")
]

def process_text(stdin, stdout):
    text = stdin.read()
    for t in replacements:
        text = text.replace(*t)
    text = filter_SI_units(text)
    stdout.write(text)
