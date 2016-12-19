from sqlalchemy import not_
from xenoliths.application import db

from xenoliths.models import ProbeMeasurement, Tag

def tagged(*tags):
    return ProbeMeasurement.tags.any(Tag.name.in_(tags))

queryset = db.session.query(ProbeMeasurement)\
    .filter(ProbeMeasurement.sample_id == "CK-1")\
    .filter(tagged("defocused"))\
    .filter(not_(tagged("exclude")))
