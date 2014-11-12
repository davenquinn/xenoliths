import os
from flask import Blueprint, request, make_response, jsonify
from json import dumps


api = Blueprint('api', __name__,)

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify(status='error', message='Not found'), 404)

@api.route('/sample/classification/<sample>', methods=["POST","GET"])
def classification(sample):
    from . import db
    from ..core.models import Sample

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
def tags(tag, points):
    from ..microprobe.models import Point
    if request.method == "POST":
        for point in points:
            pt = Point.query.get(sample=point[0], n=point[1])
            pt.tags.add(tag)

    elif request.method == "DELETE":
        for point in points:
            pt = Point.query.get(sample=point[0], n=point[1])
            pt.tags.remove(tag)
