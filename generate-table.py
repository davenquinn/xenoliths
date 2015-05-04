import numpy as N
from xenoliths.application import app, db
from xenoliths.core.models import Sample
from xenoliths.SIMS.quality import get_data
from paper.text import tex_renderer, write_file
import periodictable as pt

def mineral_data(trace_elements):
    # Check that there are the same amount of
    # measurements for each element
    n_meas = [len(d) for d in trace_elements.values()]
    n_meas = max(n_meas)

    data = {k:N.mean(v)
            for k,v in trace_elements.items()}
    data["n"] = n_meas
    return data

def averaged_trace_elements():
    trace_elements = get_data()

    for sample_id, s_data in trace_elements.items():
        data = {k:mineral_data(v)
            for k,v in s_data.items()}
        data["id"] = sample_id
        yield data

def create_table():

    data = list(averaged_trace_elements())

    atomic_number = lambda k: getattr(pt.elements,k).number
    elements = sorted([k
        for k in data[0]["cpx"].keys()
        if k != "n"], key=atomic_number)

    text = (tex_renderer
        .get_template("trace-elements.tex")
        .render(
            ncols=len(elements)+2,
            elements=elements,
            samples=data))
    write_file("build/trace-elements.tex",text)

with app.app_context():
    create_table()
