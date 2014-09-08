import os
from flask import Blueprint, request
from flask import jsonify
from json import dumps


api = Blueprint('api', __name__,)

@api.route('/sample/classification/<sample>', methods=["POST","GET"])
def classification(sample):
    from ..core.models import Sample

    sample = Sample.query.get(sample)

    if request.method == "POST":
        try:
            sample.classification = classification
            sample.save()
            return True
        except:
            return False

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
