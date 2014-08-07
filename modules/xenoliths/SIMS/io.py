from __future__ import division

import os
import json

import matplotlib.pyplot as P
import numpy as N

def load(file):
    dtype = [("el", str, 2), ("abundance", float), ("err", float)]
    return N.loadtxt(file, skiprows=2, dtype=dtype)

with open("index.json", "r") as f:
    index = json.load(f)
