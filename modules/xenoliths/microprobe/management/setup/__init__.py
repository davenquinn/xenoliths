import numpy as N
import os
from geoalchemy2.shape import from_shape
import json

from ....application import app, db
from ....models import Sample, Point
from .array import Array

def write_json():
	path = os.path.join(app.config.get("DATA_DIR"),"data.json")
	data = dict(
		type="FeatureCollection",
		features=map(lambda o: o.serialize(), Point.query.all()))
	with open(path, "w") as f:
		json.dump(data, f)

def import_sample(sample_name):
	arr = Array(sample_name+".dat")

	arr.transform_coordinates(sample_name+"_affine.txt")

	sample = Sample.get_or_create(id=sample_name)

	for rec in arr.each():
		point = Point.get_or_create(
			line_number=int(rec.id),
			sample=sample)
		point.geometry = from_shape(rec.geometry)
		point.oxides = rec.oxide_weights()
		point.errors = rec.errors()
		point.derived_data()
	db.session.commit()

def import_all():
	data_dir, samples = (app.config.get(i) for i in ("DATA_DIR", "SAMPLES"))
	os.chdir(os.path.join(data_dir,"samples"))
	for sample in samples:
		print sample
		import_sample(sample)
	write_json()

if __name__ == "__main__":
	import_all()
