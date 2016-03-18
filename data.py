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

def ree_data():

    with app.app_context():
        samples = xenoliths()

        return [ree_temperature(s,
                pressure=1.5,
                uncertainties=True,
                # Use only HREEs for CK-4 because this
                # exhibits extreme disequilibrium
                hree_only=(s.id == 'CK-4'))
                for s in samples]

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

