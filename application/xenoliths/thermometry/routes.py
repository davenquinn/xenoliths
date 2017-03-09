

import numpy as N

from matplotlib import pyplot as P
from flask import Blueprint, Response, render_template
from io import StringIO
from .results import sample_temperatures, core_temperatures
from .rare_earth.plot import plot_DREE, all_DREE, ree_temperature
from .rare_earth.calc import prepare_data, big10, rare_earths
from ..core.models import Sample
from ..microprobe.models.query import tagged, exclude_bad


thermometry = Blueprint(
    'Thermometry',
    __name__,
    static_folder="static",
    template_folder="templates")

filter_samples = lambda x: len(x.sims_measurements) > 0

def prepare_data(sample):
    t = sample_temperatures(sample)
    return dict(
        sample=sample,
        ree= ree_temperature(sample,
            pressure=1.5,
            uncertainties=True),
        bkn=t["core"]["bkn"]["single"]["val"],
        ta98_grouped=t["core"]["ta98"]["sep"],
        ta98=t["core"]["ta98"]["single"]["val"])

@thermometry.route("/")
def index():
    samples = Sample.query.filter(Sample.xenolith == True)
    data = list(map(prepare_data, samples.all()))

    return render_template("thermometry/list.html",
        title="Thermometry results (core grains)",
        data=data)

@thermometry.route("/ree/all.svg")
def ree_all():
    samples = Sample.query.all()
    fig = all_DREE(samples)
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg")
    imgdata.seek(0)
    return Response(imgdata.read(), mimetype="image/svg+xml")


@thermometry.route("/ree/<sample>.svg")
def ree_opx(sample):
    sample = Sample.query.get(sample)
    fig = plot_DREE(sample)
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg")
    imgdata.seek(0)
    return Response(imgdata.read(), mimetype="image/svg+xml")

@thermometry.route("/ree/excel-input")
def table():
    def inner():
        first = ["ID"]+big10+rare_earths+[" "]+big10+rare_earths
        yield ", ".join(first)
        samples = list(filter(filter_samples, Sample.query.all()))
        for sample in samples:
            d = prepare_data(sample)
            a = [sample.id]+d["major"]["cpx"]+d["trace"]["cpx"]+[""]+d["major"]["opx"]+d["trace"]["opx"]
            yield ", ".join([str(i) for i in a])
    a = "\n".join(list(inner()))
    return Response(a, mimetype='text')

@thermometry.route("/ree-ta98.svg")
def comparison():
    samples = Sample.query\
        .filter(Sample.xenolith == True).all()

    ree = [ree_temperature(sample,
            pressure=1.5,
            uncertainties=True).n\
            for sample in samples]
    ta98 = [N.array(core_temperatures(sample)).mean()\
            for sample in samples]

    colors = [s.color for s in samples]

    fig, ax = P.subplots()

    ax.scatter(ta98,ree, c=colors)
    ax.set_xlabel("Taylor 1998 (core)")
    ax.set_ylabel("REE-in-pyroxene")

    for x,y,s in zip(ta98,ree,samples):
        ax.annotate(s.id, (x,y), xytext=(-5,5), textcoords="offset points")

    ax.autoscale(False)
    #r = N.array(ree)
    a = [0,2000]
    ax.plot(a,a, c="#cccccc", zorder=-5)


    imgdata = StringIO()
    fig.savefig(imgdata, format="svg")
    imgdata.seek(0)
    return Response(imgdata.read(), mimetype="image/svg+xml")


