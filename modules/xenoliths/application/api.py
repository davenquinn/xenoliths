import os
from flask import Blueprint, request

from ..models import Sample, Point

api = Blueprint()

@api.route('/sample/classification/', methods=["POST","GET"])
def classification(sample):
    sample = Sample.query.get(id=sample)

    if request.method == "POST":
        try:
            sample.classification = classification
            sample.save()
            return True
        except:
            return False

    if request.method == "GET":
        s = sample.classification
        if not s: raise NotDefinedError
        return s

@api.route('/point/tag', methods=["POST","DELETE"])
def tags(tag, points):
    if request.method == "POST":
        for point in points:
            pt = Point.query.get(sample=point[0], n=point[1])
            pt.tags.add(tag)

    elif request.method == "DELETE":
        for point in points:
            pt = Point.query.get(sample=point[0], n=point[1])
            pt.tags.remove(tag)
