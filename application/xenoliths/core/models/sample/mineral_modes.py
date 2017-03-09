

import numpy as N
from flask import current_app

def get_shape(image_shape, n_cells=5000):
  # Gets the shape of an array that fits an image
  aspect_ratio = image_height / image_width
  y = N.sqrt(n_cells / aspect_ratio)
  return (round(y),round(y * aspect_ratio))

def modes(sample, completion=False):
    minerals, densities = tuple(current_app.config.get(i)\
                                for i in ("MINERALS","MINERAL_DENSITIES"))

    arr = N.array(sample.classification)
    T = arr.size
    assert T > 1

    area = {}
    for m, item in list(minerals.items()):
        mode = arr[arr == m].size/T
        if m == "na":
            na = mode
            continue
        area[m] = mode

    vol = {}
    for m, item in list(area.items()):
        vol[m] = item**1.5
    total = sum(vol.values())
    assert total > 0
    for m, item in list(vol.items()):
        vol[m] = item/total

    wt = {}
    for m, item in list(vol.items()):
        wt[m] = item*densities[m]
    total = sum(wt.values())
    for m,item in list(wt.items()):
        wt[m] = item/total

    complete = arr[arr != "un"].size/T
    if completion:
        return wt, complete
    else:
        return wt
