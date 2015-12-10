from json import dump
from xenoliths import app, db
from xenoliths.models import Sample

def classifications():
    q = db.session.query(Sample).filter_by(xenolith=True)
    for s in q.all():
        if s.classification:
            yield dict(id=s.id, cls=s.classification)

with app.app_context():
    data = list(classifications())

with open('build/classes.json','w') as f:
    dump(data, f)


