from flask import jsonify
from flask.ext.migrate import Migrate

from .base import Application
from ..database import db

app = Application(__name__)

db.init_app(app)
migrate = Migrate(app, db)

from ..microprobe.models import ProbeMeasurement
from ..thermometry.routes import thermometry
from ..SIMS import sims
from .api import api

app.register_blueprint(sims,url_prefix="/sims")
app.register_blueprint(thermometry,url_prefix="/temp")
app.register_blueprint(api,url_prefix="/api")

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/data.json")
def data():
    return jsonify(
        type="FeatureCollection",
        features=map(lambda o: o.serialize(), ProbeMeasurement.query.all()))
