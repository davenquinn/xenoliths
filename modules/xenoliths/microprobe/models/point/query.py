from ....application import app
from . import tags

def exclude_bad(query):
    """Excludes bad data from a queryset"""
    bad_tags = app.config.get("BAD_TAGS")
    return query.join(tags).filter(
        tags.c.tag_name.in_(bad_tags))
