from pickle import dump
from xenoliths import app
from xenoliths.thermometry.results import xenoliths, sample_temperatures

with app.app_context():
    data = [sample_temperatures(s)
       for s in xenoliths()]
    with open("build/data.pickle","w") as f:
        dump(data,f)
