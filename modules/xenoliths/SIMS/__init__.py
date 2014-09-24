from flask import Blueprint, Response, render_template
from cStringIO import StringIO

from .manage import SIMSCommand
from .models import Measurement, Datum
from .plot import plot_all

sims = Blueprint('SIMS', __name__, static_folder="static", template_folder="templates")

@sims.route("/list/<mineral>/")
def list(mineral):
    cols = Datum.query.distinct(Datum._element).all()
    data = Measurement.query.filter_by(mineral=mineral).all()
    return render_template("sims/list.html",
        objects=data,
        columns=[d.element for d in cols])

@sims.route("/<mineral>.svg")
def chart(mineral):
    fig = plot_all(mineral)
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg")
    imgdata.seek(0)
    return Response(imgdata.read(), mimetype="image/svg+xml")
