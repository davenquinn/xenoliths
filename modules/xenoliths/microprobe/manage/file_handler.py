import numpy as N
import re

from pathlib import Path
from pandas import read_table, concat
from .util import find_date
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

            # Temporary hack for situations when line-numbers are not unique
            # AKA different probe sessions.
            if len(point) > 1: point = point.head(1)

            cord = map(float, (point["X-POS"],point["Y-POS"]))
            tocord = (a["x"], a["y"])
            #print(u"{} -> {}".format(repr(cord),repr(tocord)))
            yield cord,tocord

    def generate_transformed():
        for sample in samples:
            try:
                coordinates = list(load_transform(sample))
            except IOError:
                print("No affine seed points available for "+sample)
                continue

            fromCoords, toCoords = zip(*list(coordinates))
            print(fromCoords,toCoords)
            affine = Affine.construct(fromCoords, toCoords, verbose=True)

            points = data[data.sample_id == sample]

            points["X-POS_affine"] = points["X-POS"]
            points["Y-POS_affine"] = points["Y-POS"]
            incoords = points[["X-POS","Y-POS"]].values
            outcords = affine.transform(incoords)
            points[["X-POS_affine","Y-POS_affine"]] = outcords
            yield points

    return concat(generate_transformed())

size_field = re.compile(r"defocused_(\d+)um")
digit_regex = re.compile(r"(\d+)")

def find_spot_size(string):
    """
    Finds the size of the probe spot used in a measurement
    given a sample name containing a string such as
    `defocused_xxx_um`
    """
    s = size_field.search(string)
    if s == None:
        return 0
    else:
        m = digit_regex.search(s.group())
        return int(m.group())

def data_frames(files):
    for path in files:
        data = read_table(str(path))
        data.columns = [s.strip() for s in data.columns]
        sample = data["SAMPLE"].str.replace("_"," ")
        splits = sample.str.split()
        data["sample_id"] = splits.str[0]
        data["group"] = splits.str[1:].str.join(" ")
        data["date"] = find_date(path.stem)
        yield data

def get_data(directory):
    data_dir = Path(directory)/"Probe"/"data"
    files = data_dir.glob("*.dat")
    data = concat(data_frames(files))

    for i,row in data.iterrows():
        row["spot_size"] = find_spot_size(row["SAMPLE"])

    return transform_coordinates(directory, data)
