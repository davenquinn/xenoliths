from ...application import app
from . import tags, Tag
from sqlalchemy.orm import aliased
from sqlalchemy import and_, not_

def tagged(query,*tags):
    from . import ProbeMeasurement
    return query.join(ProbeMeasurement.tags).filter(
        ProbeMeasurement.tags.any(Tag.name.in_(tags)))

def exclude_tagged(query,*vals):
    from . import ProbeMeasurement
    return query.join(ProbeMeasurement.tags).filter(
        ~ProbeMeasurement.tags.any(Tag.name.in_(vals)))

def exclude_bad(query,*extra_tags):
    """Excludes bad data from a queryset"""
    tags = app.config.get("BAD_TAGS")+list(extra_tags)
    return exclude_tagged(query,*tags)

