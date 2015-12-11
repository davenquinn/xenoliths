import numpy as N
from json import dump
from xenoliths import app, db
from xenoliths.models import Sample
from rasterio.features import shapes

def features(cls):
    vals = N.unique(cls)
    for i,v in enumerate(vals):
        cls[cls==v] = i

    im = cls.astype(N.uint8)
    shp = shapes(im)
    for geom,val in shp:
        yield {'v':vals[val],
                'type':'Feature',
                'geometry':geom}

def classifications():
    q = db.session.query(Sample).filter_by(xenolith=True)
    for s in q.all():
        if not s.classification:
            continue
        cls = N.array(s.classification)
        cls[cls == 'un'] = 'na'
        yield dict(
            id=s.id,
            shape=cls.shape,
            cls=list(features(cls)))

with app.app_context():
    data = list(classifications())

with open('build/classes.json','w') as f:
    dump(data, f)


