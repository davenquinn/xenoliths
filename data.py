from __future__ import division, print_function

from xenoliths import app
from xenoliths.thermometry.results import xenoliths, sample_temperatures
from pickle import dump, load

from xenoliths import app
from xenoliths.thermometry.rare_earth.plot import ree_temperature
from xenoliths.thermometry.results import xenoliths

cache = "build/comparison-data.pickle"

def create_data():
    with app.app_context():
        data = [sample_temperatures(s, distinct=min)
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


