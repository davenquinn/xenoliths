import click
from uncertainties import ufloat
from sqlalchemy import func
from xenoliths.application import app,db
from xenoliths.models import Sample, ProbeMeasurement
from xenoliths.microprobe.group import get_molar

from ..text import tex_renderer, write_file

@click.command()
def mineral_compositions():
    query = db.session.query(Sample.id)\
        .filter(Sample.xenolith == True)\
        .order_by(Sample.id)\
        .all()
    sample_ids = [s[0] for s in query]

    base_queryset = ProbeMeasurement.query\
        .join(Sample)\
        .filter(Sample.xenolith == True)\
        .exclude_bad()

    def sample_data(id):
        query = base_queryset.filter(
                ProbeMeasurement.sample_id==id)
        data = dict(id=id)
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
                molar = get_molar(qset, uncertainties=True),
                mg_number = get_number(ProbeMeasurement.mg_number),
                cr_number = get_number(ProbeMeasurement.cr_number))

        return data

    template = tex_renderer.get_template(
        "tables/minerals.tex")
    text = template.render(
        oxides=app.config.get("OXIDES"),
        samples=[sample_data(i) for i in sample_ids])
    write_file("includes/tables/minerals.tex", text)

