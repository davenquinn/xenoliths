#-*- coding: utf-8 -*-

from xenoliths.application import app
from xenoliths.microprobe.group import get_molar, get_mg_number, get_oxide_total

def describe(qset):
    fstr = "{ox:16}{val.n:6.2f} ± {val.s:1.2f} %"
    molar = get_molar(qset, uncertainties=True)
    oxides = app.config.get("OXIDES")
    print "Molar % (1σ errors)"
    for ox in oxides:
        if ox not in molar: continue
        print fstr.format(
            ox=ox, val=molar[ox])
    print ""
    print fstr.format(ox="Mg #", val=get_mg_number(qset))
    print fstr.format(ox="Oxide total", val=get_oxide_total(qset))

def make_table(queryset):
    pass
