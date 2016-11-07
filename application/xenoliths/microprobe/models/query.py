from ...application import app
from . import tags
from sqlalchemy.orm import aliased

def tagged(query,tag):
    table = aliased(tags)
    return query.join(table).filter(table.c.tag_name==tag)

def exclude_tagged(query,*vals):
    table = aliased(tags)
    return query.join(table).filter(
        table.c.tag_name.notin_(vals))

def exclude_bad(query):
    """Excludes bad data from a queryset"""
    tags = app.config.get("BAD_TAGS")
    return exclude_tagged(query,*tags)
