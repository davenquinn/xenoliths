from __future__ import division, print_function
from sqlalchemy.sql import func, distinct, select
from collections import Counter

from ..application import app, db
from ..microprobe.models import ProbeMeasurement


sql = """SELECT DISTINCT ON(g1.id)
        g1.id As gref_id,
        g2.id As gnn_id
    FROM probe_measurement As g1, probe_measurement As g2
    WHERE g1.id <> g2.id
        AND g1.sample_id = 'CK-2'
        AND g2.sample_id = 'CK-2'
        AND g1.mineral = 'opx'
        AND g2.mineral = 'cpx'
    ORDER BY g1.id, ST_Distance(g1.geometry,g2.geometry)"""

def test_distance_query():
    """ Tests querying based on distance"""
    with app.app_context():
        res = db.session.execute(sql).fetchall()

        queryset = ProbeMeasurement.query\
                .filter(ProbeMeasurement.sample_id=="CK-2")
        opx = queryset.filter(ProbeMeasurement.mineral=="opx")
        cpx = queryset.filter(ProbeMeasurement.mineral=="cpx")

        oq = opx.subquery()
        cq = cpx.subquery()

        closest = func.ST_Distance(oq.c.geometry,cq.c.geometry)
        q = select(
            [oq.c.id, cq.c.id],
            oq.c.id != cq.c.id,
            distinct=oq.c.id,
            order_by=[oq.c.id, closest])
        res2 = db.session.execute(q).fetchall()
        #print(res,res2)
        for a,b in zip(res, res2):
            print(a,b)
            assert a[0] == b[0]
            assert a[1] == b[1]

def test_distance_iterative():
    from .results import pyroxene_pairs

    def closest(queryset, measurement):
        return queryset.order_by(ProbeMeasurement.geometry\
                .ST_Distance(measurement.geometry)).first()

    def iterate_pairs(queryset):
        """ An iterative method to get the closest measurements"""
        opx = queryset.filter(ProbeMeasurement.mineral=="opx")
        cpx = queryset.filter(ProbeMeasurement.mineral=="cpx")
        if opx.count() > cpx.count():
            ls = [(closest(opx, c).id,c.id) for c in cpx.all()]
        else:
            ls = [(o.id,closest(cpx, o).id) for o in opx.all()]
        return sorted(ls, lambda a,b: b[0])

    with app.app_context():
        queryset = ProbeMeasurement.query.filter_by(sample_id="CK-2")
        pairs = iterate_pairs(queryset)
        pairs2 = [(a.id,b.id) for a,b in pyroxene_pairs(queryset)]
        print(len(pairs),len(pairs2))
        assert len(pairs) == len(pairs2)
        print("Checking uniqueness")
        assert Counter(pairs) == Counter(pairs2)

