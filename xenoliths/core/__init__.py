from pandas import read_sql
from .models import Sample
from ..application import db

def sample_colors():
    query = (db.session.query(Sample)
        .filter_by(xenolith=True)
        .order_by(Sample.id)
        .with_entities(
            Sample.id,
            Sample.color))
    colors = read_sql(
        query.statement,
        db.session.bind, index_col='id')
    colors.index.names = ['sample_id']
    return colors

