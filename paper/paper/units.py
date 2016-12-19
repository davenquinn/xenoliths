from os import path
from re import sub

__dirname = path.dirname(__file__)
with open(path.join(__dirname, 'si-units.txt')) as f:
    units = [u.rstrip() for u in f]

def filter_SI_units(text):
    for unit in units:
        text = sub("((?:(?<=\s)-)?[\d\.]+) ({})".format(unit),r"\SI{\1}{\2}",text)
    return text

