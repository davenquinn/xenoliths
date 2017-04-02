from flask import jsonify
from flask_migrate import Migrate

from .base import Application
from ..database import db

app = Application(__name__)

db.init_app(app)
migrate = Migrate(app, db)

from ..microprobe.models import ProbeMeasurement
from .api import api

app.register_blueprint(api,url_prefix="/api")

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/data.json")
def data():
    return jsonify(
        type="FeatureCollection",
        features=[o.serialize() for o in ProbeMeasurement.query.all()])
