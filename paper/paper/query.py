from __future__ import division

from uncertainties import ufloat
from sqlalchemy import func, not_
from pandas import read_sql, DataFrame
from collections import defaultdict
from itertools import chain
from xenoliths.core import sample_colors
from xenoliths.application import app,db
from xenoliths.models import Sample, ProbeMeasurement, Tag
from xenoliths.microprobe.group import average_composition

def not_bad():
    bad_tags = app.config.get("BAD_TAGS")
    return not_(
        ProbeMeasurement.tags.any(
            Tag.name.in_(bad_tags)))

def xenolith_minerals(type):
    """
    Gets the average composition of each
    mineral for all of the xenolith samples.

    :param type: Type of compositional estimate
        desired. One of `weight`,`molar`,or
        `normalized_weight`.
    """

    samples = db.session.query(Sample)\
        .filter(Sample.xenolith == True)\
        .order_by(Sample.id)\
        .all()

    base_queryset = ProbeMeasurement.query\
        .join(Sample)\
        .filter(Sample.xenolith == True)\
        .filter(not_bad())

    def sample_data(sample):
        query = base_queryset.filter(
                ProbeMeasurement.sample_id==sample.id)
        data = dict(id=sample.id)

        modes = sample.modes()

        for m in ["ol","opx","cpx","sp"]:
            qset = query.filter(
                ProbeMeasurement.mineral == m)

            get_number = lambda n: ufloat(*qset\
                .with_entities(
                    func.avg(n),
                    func.stddev(n))\
                .all()[0])

            data[m] = dict(
                count = qset.count(),
                mg_number = get_number(ProbeMeasurement.mg_number),
                cr_number = get_number(ProbeMeasurement.cr_number),
                oxide_total = get_number(ProbeMeasurement.oxide_total).n,
                mode = modes[m])

            data[m][type] = average_composition(qset,
                    type=type, uncertainties=True)

        return data

    return [sample_data(i) for i in samples]

# Maybe use molar instead?
quantity = "normalized_weight"

def rescale_values(sample_data):
    """
    Rescales computed measurements by mineral
    mode for each mineral in the sample.
    """
    n = "_number"

    sample_id = sample_data.pop("id")

    data = defaultdict(int)
    for mineral in sample_data.values():
        mode = mineral["mode"]

        items = chain(
            mineral[quantity].items(),
            ((i+n,mineral[i+n])
                for i in ("mg","cr")))

        for ox,v in items:
            data[ox] += v*mode

    data = dict(data)
    data["id"] = sample_id
    return data

def whole_rock_major_elements(dataframe=False):
    """
    Whole-rock major elements for each xenolith sample
    recalculated from oxide compositions of each mineral
    and its modal abundance.
    """
    samples = xenolith_minerals("normalized_weight")
    data = [rescale_values(sample) for sample in samples]
    if not dataframe:
        return data
    df = DataFrame.from_dict(data).set_index('id')
    return df

