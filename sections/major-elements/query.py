from xenoliths import app,db
from xenoliths.models import Sample, ProbeMeasurement, ProbeDatum
from sqlalchemy.orm.query import Query
from paper.query import not_bad
from pandas import read_sql

def partial_pivot(df):
    cols = ['measurement_id','oxide','weight_percent']
    sub = df[cols].pivot(
            index='measurement_id',
            columns='oxide')
    sub.columns = sub.columns.droplevel()

    new_cols = ['measurement_id','sample_id','color']
    f = df[new_cols]
    df = f.drop_duplicates('measurement_id')
    df.index = df.pop('measurement_id')
    return df.merge(sub,left_index=True,right_index=True)

def base_query(*entities, **kwargs):
    m = ProbeMeasurement
    d = ProbeDatum

    q = (Query(m).join(Sample)
        .filter(Sample.xenolith == True)
        .filter(m.mineral == 'sp')
        .filter(not_bad()))

    if kwargs.pop('oxides',True):
        q = q.join(d)
        entities += (
            d._oxide,
            d._cation,
            d.measurement_id)

    return q.with_entities(
        m.sample_id,
        Sample.color,
        m.session_id,
        *entities)

def spinel_data():
    q = (db.session.query(ProbeMeasurement)
        .join(Sample)
        .filter(Sample.xenolith == True)
        .filter(ProbeMeasurement.mineral == 'sp')
        .filter(not_bad()))
    return q.all()

