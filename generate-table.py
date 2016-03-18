import numpy as N
from uncertainties import ufloat
from collections import OrderedDict
from pickle import load
from paper.text import tex_renderer, write_file
from xenoliths import app
from data import ree_data

with open("build/data.pickle") as f:
    data = load(f)

template = tex_renderer.get_template("temperature.tex")

def table_data(s):
    s = OrderedDict(s.items())

    for k in ('core','rim'):
        d = s[k]

        n_opx = d['bkn']["single"].get('n_opx')
        n_cpx = d['bkn']["single"].get('n_cpx')

        # Go through thermometers
        for k_,v in d.items():
            arr = N.array(v['sep'])
            d[k_] = dict(n=arr.mean(),s=arr.std())
        d['n_cpx'] = n_cpx
        d['n_opx'] = n_opx

    ree = ree_data(s['id']).temperature
    s['core']['ree'] = dict(n=ree.n,s=ree.s)

    return s

with app.app_context():
    text = template.render(
            samples=[table_data(i) for i in data])
    write_file("build/temperatures.tex", text)
