import os
from flask import Blueprint, request,\
    make_response, jsonify, current_app
from json import dumps
from sqlalchemy.orm import joinedload

from . import db
from ..core.models import Sample
from ..microprobe.models import ProbeMeasurement, ProbeImage, Tag

api = Blueprint('api', __name__)

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify(status='error', message='Not found'), 404)

@api.route('/sample/classification/<sample>', methods=["POST","GET"])
def classification(sample):

    sample = db.session.query(Sample).get(sample)

    if request.method == "POST":
        try:
            data = request.json
            assert len(sample.classification) == len(data)
            assert len(sample.classification[0]) == len(data[0])
            sample.classification = data
            db.session.commit()
            return jsonify(status="success")
        except Exception, err:
            return jsonify(
                    status="error",
                    message=str(err),
                    data=request.json)

    if request.method == "GET":
        s = sample.classification
        if not s: raise Exception
        return dumps(s)

@api.route('/point/tag', methods=["POST","DELETE"])
def tags():
    current_app.logger.debug("tags endpoint reached")
    data = request.json

    tag = data["tag"]
    for point in data["points"]:
        pt = ProbeMeasurement.query.get(point)
        if request.method == "POST":
            pt.add_tag(tag)
        elif request.method == "DELETE":
            pt.remove_tag(tag)
    db.session.commit()

    return jsonify(
        status="success",
        data=data["points"])

@api.route('/modes')
def modes():
    def modes():
        samples = db.session.query(Sample).all()
        for s in samples:
            try:
                m, complete = s.modes(completion=True)
            except:
                continue
            yield dict(
                id=s.id,
                complete=complete,
                modes=m)

    return jsonify(
        status="success",
        data=list(modes()))

@api.route("/test")
def test():
    return jsonify(status="Success")

@api.route("/probe-data")
def probe_data():

    q = db.session.query(ProbeMeasurement)\
        .options(joinedload("data"))\
        .all()

    return jsonify(
        type="FeatureCollection",
        features=[o.serialize() for o in q])


@api.route("/probe-image")
def probe_images():
    q = db.session.query(ProbeImage).all()
    return jsonify(
        images=[im.serialize() for im in q])
