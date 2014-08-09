import numpy as N
import re

from pathlib import Path
from datetime import datetime
from pandas import read_table, concat
from .affine import Affine

def transform_coordinates(directory,data):
    samples = data["sample_id"].unique()
    data_dir = Path(directory)/"Probe"/"affine"

    def load_transform(sample):
        path = data_dir/(sample+"_affine.txt")
        affine_seed = N.loadtxt(
            str(path),
            comments="#",
            dtype=[("line_number", int), ("x", float), ("y", float)])

        points = data[data.sample_id == sample]

        for a in affine_seed:
            point = points[points.LINE==a["line_number"]]
            cord = map(float, (point["X-POS"],point["Y-POS"]))
            tocord = (a["x"], a["y"])
            print(u"{} -> {}".format(repr(cord),repr(tocord)))
            yield cord,tocord

    def generate_transformed():
        for sample in samples:
            try:
                coordinates = load_transform(sample)
            except IOError:
                print("No affine seed points available for "+sample.id)
                continue

            fromCoords, toCoords = zip(*list(coordinates))
            print(fromCoords,toCoords)
            affine = Affine.construct(fromCoords, toCoords, verbose=True)

            points = data[data.sample_id == sample]

            incoords = points[["X-POS","Y-POS"]].values
            outcords = affine.transform(incoords)
            points[["X-POS","Y-POS"]] = outcords
            yield points

    return concat(generate_transformed())

def data_frames(files):
    date_regex = re.compile(r"(\d\d-\d\d-\d\d)")
    for path in files:
        date = date_regex.search(path.stem).group()
        data = read_table(str(path))
        data.columns = [s.strip() for s in data.columns]
        sample = data["SAMPLE"].str.replace("_"," ")
        splits = sample.str.split()
        data["sample_id"] = splits.str[0]
        data["group"] = splits.str[1:].str.join(" ")
        data["date"] = datetime.strptime(date, "%m-%d-%y")
        yield data

def get_data(directory):
    data_dir = Path(directory)/"Probe"/"data"
    files = data_dir.glob("*.dat")
    data = concat(data_frames(files))
    return transform_coordinates(directory, data)
