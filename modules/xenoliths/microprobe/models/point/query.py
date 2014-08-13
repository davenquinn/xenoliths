from ....application import app
from . import tags, Point
from sqlalchemy.orm import aliased

def tagged(query,tag):
    table = aliased(tags)
    return query.join(table).filter(table.c.tag_name==tag)


def exclude_bad(query):
    """Excludes bad data from a queryset"""
    table = aliased(tags)
    bad_tags = app.config.get("BAD_TAGS")
    return query.join(table).filter(
        table.c.tag_name.notin_(bad_tags))
