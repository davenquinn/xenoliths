from __future__ import division

import numpy as N
from flask import current_app

def compute_modes(sample):
    minerals = current_app.config.get("MINERALS")
    densities = current_app.config.get("MINERAL_DENSITIES")

    arr = N.array(sample.classification)
    T = arr.size
    assert T > 1

    area = {}
    for m, item in minerals.items():
        mode = arr[arr == m].size/T
        if m == "na":
            na = mode
            continue
        area[m] = mode

    vol = {}
    for m, item in area.items():
        vol[m] = item**1.5
    total = sum(vol.itervalues())
    assert total > 0
    for m, item in vol.items():
        vol[m] = item/total

    wt = {}
    for m, item in vol.items():
        wt[m] = item*densities[m]
    total = sum(wt.itervalues())
    for m,item in wt.items():
        wt[m] = item/total

    complete = arr[arr != "un"].size/T
    return wt, complete
