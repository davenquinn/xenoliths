from __future__ import division

import numpy as N
from flask import current_app

def modes(sample, completion=False):
    minerals, densities = tuple(current_app.config.get(i)\
        for i in ("MINERALS","MINERAL_DENSITIES"))

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
    if completion:
        return wt, complete
    else:
        return wt
