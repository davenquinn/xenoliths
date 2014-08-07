from click import echo
import numpy as N
import os
from geoalchemy2.shape import from_shape
import json
import re
from pathlib import Path
from datetime import datetime
from pandas import read_table

from ....application import app, db
from ...models import Sample, Point
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


sample_regex = re.compile(r"(CK-\S+)")
date_regex = re.compile(r"(\d\d-\d\d-\d\d)")

def parse_filename(path):
	name = path.stem.replace("_"," ")
	m = sample_regex.search(name)
	date = date_regex.search(name).group()
	return dict(
		sample_id = m.group(),
		group = name[m.end()+1:]
		date = datetime.strptime(date, "%m-%d-%y"))

def import_all():
	data_dir = Path(app.config.get("RAW_DATA"))/"Probe"/"datafiles"
	files = data_dir.glob("*.dat")

	for path in files:
		file_data = parse_filename(path)
		data = read_table(str(path))

		s_id = file_data.pop("sample_id")
		assert s_id in app.config.get("SAMPLES")
		sample = Sample.get_or_create(id=s_id)



	import IPython; IPython.embed()



if __name__ == "__main__":
	import_all()
