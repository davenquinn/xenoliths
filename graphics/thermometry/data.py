from __future__ import division, print_function
import numpy as N

from xenoliths import app
from xenoliths.thermometry.results import xenoliths, sample_temperatures
from pickle import dump, load

from xenoliths.models import Sample
from xenoliths.thermometry.rare_earth.plot import ree_temperature
from xenoliths.thermometry.results import xenoliths
from xenoliths.thermometry.rare_earth import (
    ree_pyroxene, regress, temperature, rare_earths)
from collections import OrderedDict


cache = "build/comparison-data.pickle"

def create_data():
    with app.app_context():
        data = [sample_temperatures(s, distinct=min, uncertainties=True)
           for s in xenoliths()]
    with open(cache,"w") as f:
        dump(data,f)
    return data

def load_data():
    """
    Load thermometry data, creating a cache if it doesn't exist
    """
    try:
        with open(cache) as f:
            data = load(f)
    except IOError:
        data = create_data()
    return data

def sample_colors():
    with app.app_context():
        samples = xenoliths()
        return [s.color for s in samples]

with open('ree-disequilibrium.txt') as f:
    lines = (d.split() for d in f.readlines())
    for_removal = {d.pop(0):d for d in lines}

def ree_data(sample_id):

    with app.app_context():

        s = Sample.query.get(sample_id)

        s.to_remove = for_removal[s.id]
        # Index of elements to remove from regression
        ix = N.in1d(rare_earths,s.to_remove)

        s.X,s.Y = ree_pyroxene(s, 1.5) # Pressure in GPa
        s.res = regress(s.X[~ix],s.Y[~ix])
        s.temperature = temperature(s.res)
        return s

def __table_data(s):
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

def summary_data():
    with open("build/data.pickle") as f:
        data = load(f)
    return [__table_data(i) for i in data]
